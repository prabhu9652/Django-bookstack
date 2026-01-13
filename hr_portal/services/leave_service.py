"""
Leave Service - Business logic for leave management
"""

from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from ..models import LeaveRequest, LeaveBalance, LeaveType, HolidayCalendar


class LeaveService:
    """Service class for leave-related operations"""

    @staticmethod
    def calculate_leave_days(start_date, end_date, duration_type='full_day', employee=None):
        """
        Calculate total leave days excluding weekends and holidays.
        
        Args:
            start_date: Leave start date
            end_date: Leave end date
            duration_type: 'full_day', 'first_half', or 'second_half'
            employee: Employee instance (for location-based holidays)
        
        Returns:
            Decimal: Total leave days
        """
        if start_date > end_date:
            return Decimal('0')
        
        # Get holidays for the period
        holidays = set(
            HolidayCalendar.objects.filter(
                date__gte=start_date,
                date__lte=end_date,
                is_active=True
            ).values_list('date', flat=True)
        )
        
        total_days = Decimal('0')
        current_date = start_date
        
        while current_date <= end_date:
            # Skip weekends (Saturday=5, Sunday=6)
            if current_date.weekday() < 5 and current_date not in holidays:
                if current_date == start_date or current_date == end_date:
                    if duration_type in ['first_half', 'second_half']:
                        total_days += Decimal('0.5')
                    else:
                        total_days += Decimal('1')
                else:
                    total_days += Decimal('1')
            current_date += timedelta(days=1)
        
        return total_days

    @staticmethod
    @transaction.atomic
    def create_leave_request(employee, leave_data):
        """
        Create a new leave request.
        
        Args:
            employee: Employee instance
            leave_data: dict with leave request fields
        
        Returns:
            LeaveRequest instance
        """
        leave_type = leave_data['leave_type']
        start_date = leave_data['start_date']
        end_date = leave_data['end_date']
        duration_type = leave_data.get('duration_type', 'full_day')
        
        # Calculate total days
        total_days = LeaveService.calculate_leave_days(
            start_date, end_date, duration_type, employee
        )
        
        # Check leave balance
        balance = LeaveService.get_leave_balance(employee, leave_type)
        if balance and balance.available_days < total_days:
            raise ValueError(f"Insufficient leave balance. Available: {balance.available_days}, Requested: {total_days}")
        
        # Check for overlapping leaves
        overlapping = LeaveRequest.objects.filter(
            employee=employee,
            status__in=['pending', 'manager_approved', 'approved'],
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exists()
        
        if overlapping:
            raise ValueError("You have overlapping leave requests for this period")
        
        # Create request
        leave_request = LeaveRequest.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            duration_type=duration_type,
            total_days=total_days,
            reason=leave_data.get('reason', ''),
            contact_during_leave=leave_data.get('contact_during_leave', ''),
            supporting_document=leave_data.get('supporting_document'),
            status='draft'
        )
        
        return leave_request

    @staticmethod
    def get_leave_balance(employee, leave_type, year=None):
        """Get leave balance for an employee"""
        if year is None:
            year = timezone.now().year
        
        try:
            return LeaveBalance.objects.get(
                employee=employee,
                leave_type=leave_type,
                year=year
            )
        except LeaveBalance.DoesNotExist:
            # Create balance if it doesn't exist
            return LeaveBalance.objects.create(
                employee=employee,
                leave_type=leave_type,
                year=year,
                allocated_days=leave_type.default_days
            )

    @staticmethod
    def get_pending_approvals_for_manager(manager):
        """Get leave requests pending manager approval"""
        team_members = manager.direct_reports.filter(employment_status='active')
        return LeaveRequest.objects.filter(
            employee__in=team_members,
            status='pending'
        ).select_related('employee', 'leave_type')

    @staticmethod
    def get_pending_approvals_for_hr():
        """Get leave requests pending HR approval"""
        return LeaveRequest.objects.filter(
            status='manager_approved'
        ).select_related('employee', 'leave_type', 'manager_approved_by')

    @staticmethod
    def get_team_leave_calendar(manager, start_date, end_date):
        """Get team leave calendar for a date range"""
        team_members = manager.direct_reports.filter(employment_status='active')
        return LeaveRequest.objects.filter(
            employee__in=team_members,
            status='approved',
            start_date__lte=end_date,
            end_date__gte=start_date
        ).select_related('employee', 'leave_type')

    @staticmethod
    def get_employee_leave_history(employee, year=None):
        """Get leave history for an employee"""
        queryset = LeaveRequest.objects.filter(employee=employee)
        if year:
            queryset = queryset.filter(start_date__year=year)
        return queryset.select_related('leave_type').order_by('-created_at')

    @staticmethod
    @transaction.atomic
    def approve_leave_by_manager(leave_request, manager, comments=''):
        """Manager approves a leave request"""
        if leave_request.status != 'pending':
            raise ValueError("Leave request is not pending approval")
        
        # Verify manager is the reporting manager
        if leave_request.employee.reporting_manager != manager:
            raise PermissionError("You are not authorized to approve this request")
        
        leave_request.approve_by_manager(manager, comments)
        
        # Send notification to employee
        from .notification_service import NotificationService
        NotificationService.send_leave_status_notification(leave_request, 'manager_approved')
        
        return leave_request

    @staticmethod
    @transaction.atomic
    def approve_leave_by_hr(leave_request, hr_admin, comments=''):
        """HR approves a leave request (final approval)"""
        if leave_request.status != 'manager_approved':
            raise ValueError("Leave request is not pending HR approval")
        
        leave_request.approve_by_hr(hr_admin, comments)
        
        # Send notification to employee
        from .notification_service import NotificationService
        NotificationService.send_leave_status_notification(leave_request, 'approved')
        
        return leave_request

    @staticmethod
    @transaction.atomic
    def reject_leave(leave_request, rejected_by, reason):
        """Reject a leave request"""
        if leave_request.status not in ['pending', 'manager_approved']:
            raise ValueError("Leave request cannot be rejected")
        
        leave_request.reject(rejected_by, reason)
        
        # Send notification to employee
        from .notification_service import NotificationService
        NotificationService.send_leave_status_notification(leave_request, 'rejected')
        
        return leave_request
