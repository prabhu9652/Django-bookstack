"""
Expense Views - Expense management
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime

from ..permissions import (
    hr_portal_required, hr_admin_required, finance_admin_required, manager_required,
    get_employee, is_hr_admin, is_finance_admin
)
from ..models import ExpenseRequest, ExpenseCategory, Project
from ..services import ExpenseService, AuditService


@hr_portal_required
def expense_dashboard(request):
    """Expense management dashboard"""
    employee = get_employee(request.user)
    
    context = {
        'title': 'Expense Management',
        'employee': employee,
    }
    
    if employee:
        # My expense requests
        context['my_expenses'] = ExpenseRequest.objects.filter(
            employee=employee
        ).select_related('category', 'project').order_by('-created_at')[:10]
        
        # Summary
        context['expense_summary'] = ExpenseService.get_expense_summary(
            employee, year=timezone.now().year
        )
        
        # Pending approvals (for managers)
        if employee.is_manager:
            context['pending_approvals'] = ExpenseService.get_pending_approvals_for_manager(employee)
    
    # Finance pending approvals
    if is_finance_admin(request.user):
        context['finance_pending_approvals'] = ExpenseService.get_pending_approvals_for_finance()
        context['pending_payment'] = ExpenseService.get_expenses_pending_payment()
    
    return render(request, 'hr_portal/expense/dashboard.html', context)


@hr_portal_required
def expense_request_create(request):
    """Create a new expense request"""
    employee = get_employee(request.user)
    
    if not employee:
        messages.error(request, 'You must be an employee to submit expenses.')
        return redirect('hr_portal:dashboard')
    
    if request.method == 'POST':
        try:
            category = get_object_or_404(ExpenseCategory, id=request.POST.get('category'))
            
            expense_data = {
                'category': category,
                'title': request.POST.get('title'),
                'description': request.POST.get('description', ''),
                'expense_date': datetime.strptime(request.POST.get('expense_date'), '%Y-%m-%d').date(),
                'amount': request.POST.get('amount'),
                'currency': request.POST.get('currency', 'USD'),
            }
            
            if request.FILES.get('receipt'):
                expense_data['receipt'] = request.FILES['receipt']
            
            project_id = request.POST.get('project')
            if project_id:
                expense_data['project'] = get_object_or_404(Project, id=project_id)
            
            expense_request = ExpenseService.create_expense_request(employee, expense_data)
            
            # Auto-submit if requested
            if request.POST.get('submit_now'):
                expense_request.submit()
                AuditService.log_expense_action('submit', expense_request, request.user, request=request)
                messages.success(request, f'Expense claim {expense_request.request_id} submitted for approval.')
            else:
                messages.success(request, f'Expense claim {expense_request.request_id} saved as draft.')
            
            return redirect('hr_portal:expense_request_detail', request_id=expense_request.request_id)
        
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error creating expense claim: {str(e)}')
    
    context = {
        'title': 'Submit Expense',
        'categories': ExpenseCategory.objects.filter(is_active=True),
        'projects': Project.objects.filter(is_active=True),
        'currencies': ExpenseRequest.CURRENCY_CHOICES,
    }
    
    return render(request, 'hr_portal/expense/create.html', context)


@hr_portal_required
def expense_request_detail(request, request_id):
    """View expense request details"""
    expense_request = get_object_or_404(ExpenseRequest, request_id=request_id)
    employee = get_employee(request.user)
    
    # Check permissions
    can_view = (
        expense_request.employee == employee or
        is_hr_admin(request.user) or
        is_finance_admin(request.user) or
        (employee and expense_request.employee.reporting_manager == employee)
    )
    
    if not can_view:
        messages.error(request, 'You do not have permission to view this request.')
        return redirect('hr_portal:expense_dashboard')
    
    # Determine what actions are available
    can_edit = expense_request.employee == employee and expense_request.status == 'draft'
    can_submit = expense_request.employee == employee and expense_request.status == 'draft'
    can_cancel = expense_request.employee == employee and expense_request.status in ['draft', 'submitted']
    can_approve_manager = (
        employee and 
        expense_request.employee.reporting_manager == employee and 
        expense_request.status == 'submitted'
    )
    can_approve_finance = is_finance_admin(request.user) and expense_request.status == 'manager_approved'
    can_mark_paid = is_finance_admin(request.user) and expense_request.status == 'finance_approved'
    can_reject = can_approve_manager or can_approve_finance
    
    context = {
        'title': f'Expense Claim - {expense_request.request_id}',
        'expense_request': expense_request,
        'can_edit': can_edit,
        'can_submit': can_submit,
        'can_cancel': can_cancel,
        'can_approve_manager': can_approve_manager,
        'can_approve_finance': can_approve_finance,
        'can_mark_paid': can_mark_paid,
        'can_reject': can_reject,
    }
    
    return render(request, 'hr_portal/expense/detail.html', context)


@hr_portal_required
@require_POST
def expense_request_submit(request, request_id):
    """Submit an expense request for approval"""
    expense_request = get_object_or_404(ExpenseRequest, request_id=request_id)
    employee = get_employee(request.user)
    
    if expense_request.employee != employee:
        messages.error(request, 'You can only submit your own expense claims.')
        return redirect('hr_portal:expense_request_detail', request_id=request_id)
    
    if expense_request.status != 'draft':
        messages.error(request, 'Only draft claims can be submitted.')
        return redirect('hr_portal:expense_request_detail', request_id=request_id)
    
    expense_request.submit()
    AuditService.log_expense_action('submit', expense_request, request.user, request=request)
    messages.success(request, 'Expense claim submitted for approval.')
    
    return redirect('hr_portal:expense_request_detail', request_id=request_id)


@manager_required
@require_POST
def expense_approve_manager(request, request_id):
    """Manager approves an expense request"""
    expense_request = get_object_or_404(ExpenseRequest, request_id=request_id)
    employee = get_employee(request.user)
    
    try:
        comments = request.POST.get('comments', '')
        ExpenseService.approve_expense_by_manager(expense_request, employee, comments)
        AuditService.log_expense_action('approve', expense_request, request.user, comments=comments, request=request)
        messages.success(request, 'Expense claim approved.')
    except (ValueError, PermissionError) as e:
        messages.error(request, str(e))
    
    return redirect('hr_portal:expense_request_detail', request_id=request_id)


@finance_admin_required
@require_POST
def expense_approve_finance(request, request_id):
    """Finance approves an expense request"""
    expense_request = get_object_or_404(ExpenseRequest, request_id=request_id)
    employee = get_employee(request.user)
    
    try:
        comments = request.POST.get('comments', '')
        ExpenseService.approve_expense_by_finance(expense_request, employee, comments)
        AuditService.log_expense_action('approve', expense_request, request.user, comments=comments, request=request)
        messages.success(request, 'Expense claim approved.')
    except ValueError as e:
        messages.error(request, str(e))
    
    return redirect('hr_portal:expense_request_detail', request_id=request_id)


@finance_admin_required
@require_POST
def expense_mark_paid(request, request_id):
    """Mark expense as paid"""
    expense_request = get_object_or_404(ExpenseRequest, request_id=request_id)
    
    try:
        payment_reference = request.POST.get('payment_reference', '')
        ExpenseService.mark_expense_paid(expense_request, payment_reference)
        AuditService.log_expense_action('update', expense_request, request.user, comments=f'Marked as paid. Ref: {payment_reference}', request=request)
        messages.success(request, 'Expense marked as paid.')
    except ValueError as e:
        messages.error(request, str(e))
    
    return redirect('hr_portal:expense_request_detail', request_id=request_id)


@hr_portal_required
@require_POST
def expense_reject(request, request_id):
    """Reject an expense request"""
    expense_request = get_object_or_404(ExpenseRequest, request_id=request_id)
    employee = get_employee(request.user)
    
    # Check permissions
    can_reject = (
        (employee and expense_request.employee.reporting_manager == employee and expense_request.status == 'submitted') or
        (is_finance_admin(request.user) and expense_request.status == 'manager_approved')
    )
    
    if not can_reject:
        messages.error(request, 'You do not have permission to reject this request.')
        return redirect('hr_portal:expense_request_detail', request_id=request_id)
    
    reason = request.POST.get('reason', '')
    if not reason:
        messages.error(request, 'Please provide a reason for rejection.')
        return redirect('hr_portal:expense_request_detail', request_id=request_id)
    
    try:
        ExpenseService.reject_expense(expense_request, employee, reason)
        AuditService.log_expense_action('reject', expense_request, request.user, comments=reason, request=request)
        messages.success(request, 'Expense claim rejected.')
    except ValueError as e:
        messages.error(request, str(e))
    
    return redirect('hr_portal:expense_request_detail', request_id=request_id)


@hr_portal_required
def expense_history(request):
    """View expense history"""
    employee = get_employee(request.user)
    
    if not employee:
        return redirect('hr_portal:dashboard')
    
    year = request.GET.get('year', timezone.now().year)
    expenses = ExpenseService.get_employee_expense_history(employee, year=int(year))
    
    context = {
        'title': 'Expense History',
        'expenses': expenses,
        'selected_year': int(year),
        'years': range(timezone.now().year, timezone.now().year - 5, -1),
    }
    
    return render(request, 'hr_portal/expense/history.html', context)
