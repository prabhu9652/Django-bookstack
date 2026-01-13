"""
Leave Views - Leave management
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime
import json

from ..permissions import (
    hr_portal_required, hr_admin_required, manager_required,
    get_employee, is_hr_admin, is_manager
)
from ..models import LeaveRequest, LeaveType, LeaveBalance, HolidayCalendar
from ..services import LeaveService, AuditService


@hr_portal_required
def leave_dashboard(request):
    """Leave management dashboard"""
    employee = get_employee(request.user)
    current_year = timezone.now().year
    
    context = {
        'title': 'Leave Management',
        'employee': employee,
    }
    
    if employee:
        # Leave balances
        context['leave_balances'] = LeaveBalance.objects.filter(
            employee=employee,
            year=current_year
        ).select_related('leave_type')
        
        # My leave requests
        context['my_leaves'] = LeaveRequest.objects.filter(
            employee=employee
        ).select_related('leave_type').order_by('-created_at')[:10]
        
        # Pending approvals (for managers)
        if employee.is_manager:
            context['pending_approvals'] = LeaveService.get_pending_approvals_for_manager(employee)
    
    # HR pending approvals
    if is_hr_admin(request.user):
        context['hr_pending_approvals'] = LeaveService.get_pending_approvals_for_hr()
    
    return render(request, 'hr_portal/leave/dashboard.html', context)


@hr_portal_required
def leave_request_create(request):
    """Create a new leave request"""
    employee = get_employee(request.user)
    
    if not employee:
        messages.error(request, 'You must be an employee to request leave.')
        return redirect('hr_portal:dashboard')
    
    if request.method == 'POST':
        try:
            leave_type = get_object_or_404(LeaveType, id=request.POST.get('leave_type'))
            start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()
            
            leave_data = {
                'leave_type': leave_type,
                'start_date': start_date,
                'end_date': end_date,
                'duration_type': request.POST.get('duration_type', 'full_day'),
                'reason': request.POST.get('reason', ''),
                'contact_during_leave': request.POST.get('contact_during_leave', ''),
            }
            
            if request.FILES.get('supporting_document'):
                leave_data['supporting_document'] = request.FILES['supporting_document']
            
            leave_request = LeaveService.create_leave_request(employee, leave_data)
            
            # Auto-submit if requested
            if request.POST.get('submit_now'):
                leave_request.submit()
                AuditService.log_leave_action('submit', leave_request, request.user, request=request)
                messages.success(request, f'Leave request {leave_request.request_id} submitted for approval.')
            else:
                messages.success(request, f'Leave request {leave_request.request_id} saved as draft.')
            
            return redirect('hr_portal:leave_request_detail', request_id=leave_request.request_id)
        
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error creating leave request: {str(e)}')
    
    current_year = timezone.now().year
    
    context = {
        'title': 'Request Leave',
        'leave_types': LeaveType.objects.filter(is_active=True),
        'leave_balances': LeaveBalance.objects.filter(
            employee=employee,
            year=current_year
        ).select_related('leave_type'),
        'duration_types': LeaveRequest.DURATION_TYPE_CHOICES,
    }
    
    return render(request, 'hr_portal/leave/create.html', context)


@hr_portal_required
def leave_request_detail(request, request_id):
    """View leave request details"""
    leave_request = get_object_or_404(LeaveRequest, request_id=request_id)
    employee = get_employee(request.user)
    
    # Check permissions
    can_view = (
        leave_request.employee == employee or
        is_hr_admin(request.user) or
        (employee and leave_request.employee.reporting_manager == employee)
    )
    
    if not can_view:
        messages.error(request, 'You do not have permission to view this request.')
        return redirect('hr_portal:leave_dashboard')
    
    # Determine what actions are available
    can_edit = leave_request.employee == employee and leave_request.status == 'draft'
    can_submit = leave_request.employee == employee and leave_request.status == 'draft'
    can_cancel = leave_request.employee == employee and leave_request.status in ['draft', 'pending', 'manager_approved']
    can_approve_manager = (
        employee and 
        leave_request.employee.reporting_manager == employee and 
        leave_request.status == 'pending'
    )
    can_approve_hr = is_hr_admin(request.user) and leave_request.status == 'manager_approved'
    can_reject = can_approve_manager or can_approve_hr
    
    context = {
        'title': f'Leave Request - {leave_request.request_id}',
        'leave_request': leave_request,
        'can_edit': can_edit,
        'can_submit': can_submit,
        'can_cancel': can_cancel,
        'can_approve_manager': can_approve_manager,
        'can_approve_hr': can_approve_hr,
        'can_reject': can_reject,
    }
    
    return render(request, 'hr_portal/leave/detail.html', context)


@hr_portal_required
@require_POST
def leave_request_submit(request, request_id):
    """Submit a leave request for approval"""
    leave_request = get_object_or_404(LeaveRequest, request_id=request_id)
    employee = get_employee(request.user)
    
    if leave_request.employee != employee:
        messages.error(request, 'You can only submit your own leave requests.')
        return redirect('hr_portal:leave_request_detail', request_id=request_id)
    
    if leave_request.status != 'draft':
        messages.error(request, 'Only draft requests can be submitted.')
        return redirect('hr_portal:leave_request_detail', request_id=request_id)
    
    leave_request.submit()
    AuditService.log_leave_action('submit', leave_request, request.user, request=request)
    messages.success(request, 'Leave request submitted for approval.')
    
    return redirect('hr_portal:leave_request_detail', request_id=request_id)


@hr_portal_required
@require_POST
def leave_request_cancel(request, request_id):
    """Cancel a leave request"""
    leave_request = get_object_or_404(LeaveRequest, request_id=request_id)
    employee = get_employee(request.user)
    
    if leave_request.employee != employee:
        messages.error(request, 'You can only cancel your own leave requests.')
        return redirect('hr_portal:leave_request_detail', request_id=request_id)
    
    if leave_request.status not in ['draft', 'pending', 'manager_approved']:
        messages.error(request, 'This request cannot be cancelled.')
        return redirect('hr_portal:leave_request_detail', request_id=request_id)
    
    leave_request.cancel()
    AuditService.log_leave_action('cancel', leave_request, request.user, request=request)
    messages.success(request, 'Leave request cancelled.')
    
    return redirect('hr_portal:leave_dashboard')


@manager_required
@require_POST
def leave_approve_manager(request, request_id):
    """Manager approves a leave request"""
    leave_request = get_object_or_404(LeaveRequest, request_id=request_id)
    employee = get_employee(request.user)
    
    try:
        comments = request.POST.get('comments', '')
        LeaveService.approve_leave_by_manager(leave_request, employee, comments)
        AuditService.log_leave_action('approve', leave_request, request.user, comments=comments, request=request)
        messages.success(request, 'Leave request approved.')
    except (ValueError, PermissionError) as e:
        messages.error(request, str(e))
    
    return redirect('hr_portal:leave_request_detail', request_id=request_id)


@hr_admin_required
@require_POST
def leave_approve_hr(request, request_id):
    """HR approves a leave request (final approval)"""
    leave_request = get_object_or_404(LeaveRequest, request_id=request_id)
    employee = get_employee(request.user)
    
    try:
        comments = request.POST.get('comments', '')
        LeaveService.approve_leave_by_hr(leave_request, employee, comments)
        AuditService.log_leave_action('approve', leave_request, request.user, comments=comments, request=request)
        messages.success(request, 'Leave request approved.')
    except ValueError as e:
        messages.error(request, str(e))
    
    return redirect('hr_portal:leave_request_detail', request_id=request_id)


@hr_portal_required
@require_POST
def leave_reject(request, request_id):
    """Reject a leave request"""
    leave_request = get_object_or_404(LeaveRequest, request_id=request_id)
    employee = get_employee(request.user)
    
    # Check permissions
    can_reject = (
        (employee and leave_request.employee.reporting_manager == employee and leave_request.status == 'pending') or
        (is_hr_admin(request.user) and leave_request.status == 'manager_approved')
    )
    
    if not can_reject:
        messages.error(request, 'You do not have permission to reject this request.')
        return redirect('hr_portal:leave_request_detail', request_id=request_id)
    
    reason = request.POST.get('reason', '')
    if not reason:
        messages.error(request, 'Please provide a reason for rejection.')
        return redirect('hr_portal:leave_request_detail', request_id=request_id)
    
    try:
        LeaveService.reject_leave(leave_request, employee, reason)
        AuditService.log_leave_action('reject', leave_request, request.user, comments=reason, request=request)
        messages.success(request, 'Leave request rejected.')
    except ValueError as e:
        messages.error(request, str(e))
    
    return redirect('hr_portal:leave_request_detail', request_id=request_id)


@hr_portal_required
def leave_history(request):
    """View leave history"""
    employee = get_employee(request.user)
    
    if not employee:
        return redirect('hr_portal:dashboard')
    
    year = request.GET.get('year', timezone.now().year)
    leaves = LeaveService.get_employee_leave_history(employee, year=int(year))
    
    context = {
        'title': 'Leave History',
        'leaves': leaves,
        'selected_year': int(year),
        'years': range(timezone.now().year, timezone.now().year - 5, -1),
    }
    
    return render(request, 'hr_portal/leave/history.html', context)


@hr_portal_required
def leave_calendar(request):
    """View leave calendar"""
    employee = get_employee(request.user)
    
    context = {
        'title': 'Leave Calendar',
        'employee': employee,
    }
    
    return render(request, 'hr_portal/leave/calendar.html', context)


# API endpoints
@hr_portal_required
def api_calculate_leave_days(request):
    """Calculate leave days for a date range"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    duration_type = request.GET.get('duration_type', 'full_day')
    
    if not start_date or not end_date:
        return JsonResponse({'error': 'Start and end dates are required'}, status=400)
    
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        employee = get_employee(request.user)
        days = LeaveService.calculate_leave_days(start, end, duration_type, employee)
        
        return JsonResponse({'days': float(days)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@hr_portal_required
def api_get_leave_balance(request, leave_type_id):
    """Get leave balance for a leave type"""
    employee = get_employee(request.user)
    
    if not employee:
        return JsonResponse({'error': 'Employee not found'}, status=404)
    
    leave_type = get_object_or_404(LeaveType, id=leave_type_id)
    balance = LeaveService.get_leave_balance(employee, leave_type)
    
    return JsonResponse({
        'allocated': float(balance.allocated_days),
        'used': float(balance.used_days),
        'available': float(balance.available_days),
    })
