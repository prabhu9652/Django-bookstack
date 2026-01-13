"""
Dashboard Views - Main HR Portal dashboard and navigation
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from ..permissions import hr_portal_required, get_employee, is_hr_admin, is_manager
from ..models import (
    LeaveRequest, ExpenseRequest, Timesheet, Asset, 
    HolidayCalendar, Notification, Employee
)
from ..services import NotificationService


@hr_portal_required
def dashboard(request):
    """Main HR Portal dashboard"""
    user = request.user
    employee = get_employee(user)
    
    context = {
        'title': 'HR Portal Dashboard',
        'employee': employee,
    }
    
    if employee:
        # Employee dashboard data
        current_year = timezone.now().year
        today = timezone.now().date()
        
        # Leave balances
        context['leave_balances'] = employee.leave_balances.filter(year=current_year).select_related('leave_type')
        
        # Pending requests
        context['pending_leaves'] = LeaveRequest.objects.filter(
            employee=employee,
            status__in=['pending', 'manager_approved']
        ).count()
        
        context['pending_expenses'] = ExpenseRequest.objects.filter(
            employee=employee,
            status__in=['submitted', 'manager_approved']
        ).count()
        
        # Recent requests
        context['recent_leaves'] = LeaveRequest.objects.filter(
            employee=employee
        ).select_related('leave_type').order_by('-created_at')[:5]
        
        context['recent_expenses'] = ExpenseRequest.objects.filter(
            employee=employee
        ).select_related('category').order_by('-created_at')[:5]
        
        # Assigned assets
        context['assigned_assets'] = Asset.objects.filter(
            assigned_to=employee
        ).select_related('category')[:5]
        
        # Upcoming holidays
        context['upcoming_holidays'] = HolidayCalendar.objects.filter(
            date__gte=today,
            date__lte=today + timedelta(days=30),
            is_active=True
        ).order_by('date')[:5]
        
        # Team on leave (for managers)
        if employee.is_manager:
            team_members = employee.direct_reports.filter(employment_status='active')
            context['team_on_leave'] = LeaveRequest.objects.filter(
                employee__in=team_members,
                status='approved',
                start_date__lte=today,
                end_date__gte=today
            ).select_related('employee', 'leave_type')
        
        # Pending approvals (for managers)
        if employee.is_manager:
            team_members = employee.direct_reports.filter(employment_status='active')
            context['pending_leave_approvals'] = LeaveRequest.objects.filter(
                employee__in=team_members,
                status='pending'
            ).count()
            
            context['pending_expense_approvals'] = ExpenseRequest.objects.filter(
                employee__in=team_members,
                status='submitted'
            ).count()
            
            context['pending_timesheet_approvals'] = Timesheet.objects.filter(
                employee__in=team_members,
                status='submitted'
            ).count()
    
    # HR Admin dashboard data
    if is_hr_admin(user):
        context['hr_pending_leaves'] = LeaveRequest.objects.filter(
            status='manager_approved'
        ).count()
        
        context['total_employees'] = Employee.objects.filter(
            employment_status='active'
        ).count()
        
        context['new_employees_this_month'] = Employee.objects.filter(
            joining_date__month=timezone.now().month,
            joining_date__year=timezone.now().year
        ).count()
    
    # Notifications
    context['notifications'] = NotificationService.get_unread_notifications(user, limit=5)
    context['unread_count'] = NotificationService.get_unread_count(user)
    
    return render(request, 'hr_portal/dashboard.html', context)


@hr_portal_required
def notifications(request):
    """View all notifications"""
    notifications = NotificationService.get_all_notifications(request.user, limit=100)
    
    context = {
        'title': 'Notifications',
        'notifications': notifications,
    }
    
    return render(request, 'hr_portal/notifications.html', context)


@hr_portal_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    NotificationService.mark_as_read(notification_id, request.user)
    return redirect(request.META.get('HTTP_REFERER', 'hr_portal:dashboard'))


@hr_portal_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    NotificationService.mark_all_as_read(request.user)
    return redirect('hr_portal:notifications')


@hr_portal_required
def my_profile(request):
    """View/edit employee profile"""
    employee = get_employee(request.user)
    
    if not employee:
        return redirect('hr_portal:dashboard')
    
    context = {
        'title': 'My Profile',
        'employee': employee,
        'reporting_chain': employee.get_reporting_chain(),
    }
    
    return render(request, 'hr_portal/profile.html', context)
