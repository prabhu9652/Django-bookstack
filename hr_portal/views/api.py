"""
API Views - REST API endpoints for HR Portal
"""

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from ..permissions import hr_portal_required, get_employee, is_hr_admin
from ..models import (
    Employee, LeaveRequest, ExpenseRequest, Timesheet, 
    Notification, HolidayCalendar
)


@hr_portal_required
@require_GET
def api_employee_search(request):
    """Search employees by name or ID"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    employees = Employee.objects.filter(
        models.Q(employee_id__icontains=query) |
        models.Q(user__first_name__icontains=query) |
        models.Q(user__last_name__icontains=query) |
        models.Q(user__username__icontains=query),
        employment_status='active'
    ).select_related('user', 'department')[:10]
    
    results = [{
        'id': e.id,
        'employee_id': e.employee_id,
        'name': e.full_name,
        'department': e.department.name,
    } for e in employees]
    
    return JsonResponse({'results': results})


@hr_portal_required
@require_GET
def api_notifications(request):
    """Get user notifications"""
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).order_by('-created_at')[:10]
    
    results = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'type': n.notification_type,
        'link': n.link,
        'created_at': n.created_at.isoformat(),
    } for n in notifications]
    
    return JsonResponse({
        'notifications': results,
        'unread_count': notifications.count()
    })


@hr_portal_required
@require_POST
def api_mark_notification_read(request, notification_id):
    """Mark notification as read"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.mark_as_read()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)


@hr_portal_required
@require_GET
def api_leave_balance(request):
    """Get current user's leave balances"""
    employee = get_employee(request.user)
    
    if not employee:
        return JsonResponse({'error': 'Not an employee'}, status=403)
    
    from ..models import LeaveBalance, LeaveType
    year = timezone.now().year
    
    balances = []
    for leave_type in LeaveType.objects.filter(is_active=True):
        balance, _ = LeaveBalance.objects.get_or_create(
            employee=employee,
            leave_type=leave_type,
            year=year,
            defaults={'allocated_days': leave_type.default_days}
        )
        balances.append({
            'type': leave_type.name,
            'code': leave_type.code,
            'allocated': float(balance.allocated_days),
            'used': float(balance.used_days),
            'available': float(balance.available_days),
        })
    
    return JsonResponse({'balances': balances, 'year': year})


@hr_portal_required
@require_GET
def api_holidays(request):
    """Get holidays for a year"""
    year = int(request.GET.get('year', timezone.now().year))
    
    holidays = HolidayCalendar.objects.filter(
        year=year, is_active=True
    ).order_by('date')
    
    results = [{
        'name': h.name,
        'date': h.date.isoformat(),
        'type': h.holiday_type,
        'location': h.location,
    } for h in holidays]
    
    return JsonResponse({'holidays': results, 'year': year})


@hr_portal_required
@require_GET
def api_dashboard_stats(request):
    """Get dashboard statistics"""
    employee = get_employee(request.user)
    
    stats = {
        'pending_leaves': 0,
        'pending_expenses': 0,
        'pending_timesheets': 0,
    }
    
    if employee:
        stats['pending_leaves'] = LeaveRequest.objects.filter(
            employee=employee, status__in=['pending', 'manager_approved']
        ).count()
        stats['pending_expenses'] = ExpenseRequest.objects.filter(
            employee=employee, status__in=['submitted', 'manager_approved']
        ).count()
        stats['pending_timesheets'] = Timesheet.objects.filter(
            employee=employee, status='submitted'
        ).count()
    
    return JsonResponse(stats)


# Import models for queries
from django.db import models
