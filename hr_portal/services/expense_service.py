"""
Expense Service - Business logic for expense management
"""

from django.db import transaction
from django.utils import timezone
from ..models import ExpenseRequest, ExpenseCategory


class ExpenseService:
    """Service class for expense-related operations"""

    @staticmethod
    @transaction.atomic
    def create_expense_request(employee, expense_data):
        """
        Create a new expense request.
        
        Args:
            employee: Employee instance
            expense_data: dict with expense request fields
        
        Returns:
            ExpenseRequest instance
        """
        category = expense_data['category']
        amount = expense_data['amount']
        
        # Validate against category max amount
        if category.max_amount and amount > category.max_amount:
            raise ValueError(f"Amount exceeds category limit of {category.max_amount}")
        
        # Check if receipt is required
        if category.requires_receipt and not expense_data.get('receipt'):
            raise ValueError("Receipt is required for this expense category")
        
        expense_request = ExpenseRequest.objects.create(
            employee=employee,
            category=category,
            title=expense_data['title'],
            description=expense_data.get('description', ''),
            expense_date=expense_data['expense_date'],
            amount=amount,
            currency=expense_data.get('currency', 'USD'),
            receipt=expense_data.get('receipt'),
            project=expense_data.get('project'),
            status='draft'
        )
        
        return expense_request

    @staticmethod
    def get_pending_approvals_for_manager(manager):
        """Get expense requests pending manager approval"""
        team_members = manager.direct_reports.filter(employment_status='active')
        return ExpenseRequest.objects.filter(
            employee__in=team_members,
            status='submitted'
        ).select_related('employee', 'category', 'project')

    @staticmethod
    def get_pending_approvals_for_finance():
        """Get expense requests pending finance approval"""
        return ExpenseRequest.objects.filter(
            status='manager_approved'
        ).select_related('employee', 'category', 'project', 'manager_approved_by')

    @staticmethod
    def get_expenses_pending_payment():
        """Get approved expenses pending payment"""
        return ExpenseRequest.objects.filter(
            status='finance_approved'
        ).select_related('employee', 'category')

    @staticmethod
    def get_employee_expense_history(employee, year=None):
        """Get expense history for an employee"""
        queryset = ExpenseRequest.objects.filter(employee=employee)
        if year:
            queryset = queryset.filter(expense_date__year=year)
        return queryset.select_related('category', 'project').order_by('-created_at')

    @staticmethod
    def get_expense_summary(employee, year=None):
        """Get expense summary for an employee"""
        from django.db.models import Sum, Count
        
        queryset = ExpenseRequest.objects.filter(employee=employee)
        if year:
            queryset = queryset.filter(expense_date__year=year)
        
        return {
            'total_submitted': queryset.filter(status__in=['submitted', 'manager_approved', 'finance_approved', 'paid']).aggregate(
                total=Sum('amount'), count=Count('id')
            ),
            'total_approved': queryset.filter(status__in=['finance_approved', 'paid']).aggregate(
                total=Sum('amount'), count=Count('id')
            ),
            'total_paid': queryset.filter(status='paid').aggregate(
                total=Sum('amount'), count=Count('id')
            ),
            'pending': queryset.filter(status__in=['submitted', 'manager_approved']).aggregate(
                total=Sum('amount'), count=Count('id')
            ),
            'by_category': queryset.filter(status='paid').values('category__name').annotate(
                total=Sum('amount'), count=Count('id')
            ),
        }

    @staticmethod
    @transaction.atomic
    def approve_expense_by_manager(expense_request, manager, comments=''):
        """Manager approves an expense request"""
        if expense_request.status != 'submitted':
            raise ValueError("Expense request is not pending approval")
        
        # Verify manager is the reporting manager
        if expense_request.employee.reporting_manager != manager:
            raise PermissionError("You are not authorized to approve this request")
        
        expense_request.approve_by_manager(manager, comments)
        
        # Send notification
        from .notification_service import NotificationService
        NotificationService.send_expense_status_notification(expense_request, 'manager_approved')
        
        return expense_request

    @staticmethod
    @transaction.atomic
    def approve_expense_by_finance(expense_request, finance_admin, comments=''):
        """Finance approves an expense request"""
        if expense_request.status != 'manager_approved':
            raise ValueError("Expense request is not pending finance approval")
        
        expense_request.approve_by_finance(finance_admin, comments)
        
        # Send notification
        from .notification_service import NotificationService
        NotificationService.send_expense_status_notification(expense_request, 'finance_approved')
        
        return expense_request

    @staticmethod
    @transaction.atomic
    def mark_expense_paid(expense_request, payment_reference=''):
        """Mark expense as paid"""
        if expense_request.status != 'finance_approved':
            raise ValueError("Expense request is not approved for payment")
        
        expense_request.mark_paid(payment_reference)
        
        # Send notification
        from .notification_service import NotificationService
        NotificationService.send_expense_status_notification(expense_request, 'paid')
        
        return expense_request

    @staticmethod
    @transaction.atomic
    def reject_expense(expense_request, rejected_by, reason):
        """Reject an expense request"""
        if expense_request.status not in ['submitted', 'manager_approved']:
            raise ValueError("Expense request cannot be rejected")
        
        expense_request.reject(rejected_by, reason)
        
        # Send notification
        from .notification_service import NotificationService
        NotificationService.send_expense_status_notification(expense_request, 'rejected')
        
        return expense_request
