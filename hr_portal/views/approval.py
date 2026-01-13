"""
Approval Views - Approval workflow management
"""

from django.shortcuts import render, redirect
from django.utils import timezone

from ..permissions import (
    hr_portal_required, hr_admin_required, finance_admin_required, manager_required,
    get_employee, is_hr_admin, is_finance_admin
)
from ..models import LeaveRequest, ExpenseRequest, Timesheet
from ..services import LeaveService, ExpenseService, TimesheetService


@hr_portal_required
def approval_dashboard(request):
    """Unified approval dashboard"""
    employee = get_employee(request.user)
    
    context = {
        'title': 'Approvals',
        'employee': employee,
        'pending_leaves': [],
        'pending_expenses': [],
        'pending_timesheets': [],
    }
    
    # Manager approvals
    if employee and employee.is_manager:
        context['pending_leaves'] = LeaveService.get_pending_approvals_for_manager(employee)
        context['pending_expenses'] = ExpenseService.get_pending_approvals_for_manager(employee)
        context['pending_timesheets'] = TimesheetService.get_pending_approvals_for_manager(employee)
    
    # HR approvals
    if is_hr_admin(request.user):
        context['hr_pending_leaves'] = LeaveService.get_pending_approvals_for_hr()
    
    # Finance approvals
    if is_finance_admin(request.user):
        context['finance_pending_expenses'] = ExpenseService.get_pending_approvals_for_finance()
        context['expenses_pending_payment'] = ExpenseService.get_expenses_pending_payment()
    
    return render(request, 'hr_portal/approval/dashboard.html', context)
