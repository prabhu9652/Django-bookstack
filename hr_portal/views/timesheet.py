"""
Timesheet Views - Time tracking and management
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from ..permissions import (
    hr_portal_required, manager_required, hr_admin_required,
    get_employee, is_hr_admin
)
from ..models import Timesheet, TimesheetEntry, Project, ProjectAssignment
from ..services import TimesheetService, AuditService


@hr_portal_required
def timesheet_dashboard(request):
    """Timesheet management dashboard"""
    employee = get_employee(request.user)
    
    context = {
        'title': 'Timesheet Management',
        'employee': employee,
    }
    
    if employee:
        # Current week timesheet
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        context['current_timesheet'], _ = TimesheetService.get_or_create_timesheet(employee, week_start)
        
        # Recent timesheets
        context['recent_timesheets'] = Timesheet.objects.filter(
            employee=employee
        ).order_by('-week_start_date')[:10]
        
        # Assigned projects
        context['assigned_projects'] = ProjectAssignment.objects.filter(
            employee=employee, is_active=True
        ).select_related('project')
        
        # Pending approvals (for managers)
        if employee.is_manager:
            context['pending_approvals'] = TimesheetService.get_pending_approvals_for_manager(employee)
    
    return render(request, 'hr_portal/timesheet/dashboard.html', context)


@hr_portal_required
def timesheet_detail(request, timesheet_id):
    """View/edit timesheet details"""
    timesheet = get_object_or_404(Timesheet, id=timesheet_id)
    employee = get_employee(request.user)
    
    # Check permissions
    can_view = (
        timesheet.employee == employee or
        is_hr_admin(request.user) or
        (employee and timesheet.employee.reporting_manager == employee)
    )
    
    if not can_view:
        messages.error(request, 'You do not have permission to view this timesheet.')
        return redirect('hr_portal:timesheet_dashboard')
    
    can_edit = timesheet.employee == employee and timesheet.status == 'draft'
    can_submit = timesheet.employee == employee and timesheet.status == 'draft'
    can_approve = (
        employee and 
        timesheet.employee.reporting_manager == employee and 
        timesheet.status == 'submitted'
    )
    
    # Get entries grouped by date
    entries = timesheet.entries.select_related('project').order_by('date', 'project')
    
    # Get available projects for this employee
    assigned_projects = Project.objects.filter(
        assignments__employee=timesheet.employee,
        assignments__is_active=True,
        is_active=True
    ).distinct()
    
    context = {
        'title': f'Timesheet - Week of {timesheet.week_start_date}',
        'timesheet': timesheet,
        'entries': entries,
        'assigned_projects': assigned_projects,
        'can_edit': can_edit,
        'can_submit': can_submit,
        'can_approve': can_approve,
    }
    
    return render(request, 'hr_portal/timesheet/detail.html', context)


@hr_portal_required
@require_POST
def timesheet_add_entry(request, timesheet_id):
    """Add entry to timesheet"""
    timesheet = get_object_or_404(Timesheet, id=timesheet_id)
    employee = get_employee(request.user)
    
    if timesheet.employee != employee:
        messages.error(request, 'You can only edit your own timesheets.')
        return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet_id)
    
    if timesheet.status != 'draft':
        messages.error(request, 'Cannot edit a submitted timesheet.')
        return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet_id)
    
    try:
        project = get_object_or_404(Project, id=request.POST.get('project'))
        entry_date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
        hours = Decimal(request.POST.get('hours', '0'))
        description = request.POST.get('description', '')
        is_billable = request.POST.get('is_billable') == 'on'
        
        # Validate date is within timesheet week
        if not (timesheet.week_start_date <= entry_date <= timesheet.week_end_date):
            raise ValueError('Date must be within the timesheet week')
        
        TimesheetEntry.objects.create(
            timesheet=timesheet,
            project=project,
            date=entry_date,
            hours=hours,
            description=description,
            is_billable=is_billable
        )
        
        messages.success(request, 'Entry added successfully.')
    except ValueError as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, f'Error adding entry: {str(e)}')
    
    return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet_id)


@hr_portal_required
@require_POST
def timesheet_delete_entry(request, entry_id):
    """Delete timesheet entry"""
    entry = get_object_or_404(TimesheetEntry, id=entry_id)
    timesheet = entry.timesheet
    employee = get_employee(request.user)
    
    if timesheet.employee != employee:
        messages.error(request, 'You can only edit your own timesheets.')
        return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet.id)
    
    if timesheet.status != 'draft':
        messages.error(request, 'Cannot edit a submitted timesheet.')
        return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet.id)
    
    entry.delete()
    messages.success(request, 'Entry deleted.')
    
    return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet.id)


@hr_portal_required
@require_POST
def timesheet_submit(request, timesheet_id):
    """Submit timesheet for approval"""
    timesheet = get_object_or_404(Timesheet, id=timesheet_id)
    employee = get_employee(request.user)
    
    if timesheet.employee != employee:
        messages.error(request, 'You can only submit your own timesheets.')
        return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet_id)
    
    if timesheet.status != 'draft':
        messages.error(request, 'Timesheet has already been submitted.')
        return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet_id)
    
    if not timesheet.entries.exists():
        messages.error(request, 'Cannot submit an empty timesheet.')
        return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet_id)
    
    timesheet.submit()
    AuditService.log_timesheet_action('submit', timesheet, request.user, request=request)
    messages.success(request, 'Timesheet submitted for approval.')
    
    return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet_id)


@manager_required
@require_POST
def timesheet_approve(request, timesheet_id):
    """Approve timesheet"""
    timesheet = get_object_or_404(Timesheet, id=timesheet_id)
    employee = get_employee(request.user)
    
    try:
        comments = request.POST.get('comments', '')
        TimesheetService.approve_timesheet(timesheet, employee, comments)
        AuditService.log_timesheet_action('approve', timesheet, request.user, comments=comments, request=request)
        messages.success(request, 'Timesheet approved.')
    except (ValueError, PermissionError) as e:
        messages.error(request, str(e))
    
    return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet_id)


@manager_required
@require_POST
def timesheet_reject(request, timesheet_id):
    """Reject timesheet"""
    timesheet = get_object_or_404(Timesheet, id=timesheet_id)
    employee = get_employee(request.user)
    
    reason = request.POST.get('reason', '')
    if not reason:
        messages.error(request, 'Please provide a reason for rejection.')
        return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet_id)
    
    try:
        TimesheetService.reject_timesheet(timesheet, employee, reason)
        AuditService.log_timesheet_action('reject', timesheet, request.user, comments=reason, request=request)
        messages.success(request, 'Timesheet rejected.')
    except (ValueError, PermissionError) as e:
        messages.error(request, str(e))
    
    return redirect('hr_portal:timesheet_detail', timesheet_id=timesheet_id)


@hr_portal_required
def timesheet_history(request):
    """View timesheet history"""
    employee = get_employee(request.user)
    
    if not employee:
        return redirect('hr_portal:dashboard')
    
    year = request.GET.get('year', timezone.now().year)
    timesheets = Timesheet.objects.filter(
        employee=employee,
        week_start_date__year=int(year)
    ).order_by('-week_start_date')
    
    context = {
        'title': 'Timesheet History',
        'timesheets': timesheets,
        'selected_year': int(year),
        'years': range(timezone.now().year, timezone.now().year - 5, -1),
    }
    
    return render(request, 'hr_portal/timesheet/history.html', context)
