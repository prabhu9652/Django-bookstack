"""
Project Views - Project management for HR
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime
from decimal import Decimal

from ..permissions import (
    hr_portal_required, hr_admin_required,
    get_employee, is_hr_admin, can_manage_projects
)
from ..models import Project, ProjectAssignment, Employee, Department, TimesheetEntry
from ..services import AuditService


@hr_portal_required
def project_dashboard(request):
    """Project management dashboard"""
    employee = get_employee(request.user)
    
    context = {
        'title': 'Project Management',
        'employee': employee,
    }
    
    if employee:
        # My project assignments
        context['my_projects'] = ProjectAssignment.objects.filter(
            employee=employee, is_active=True
        ).select_related('project')
        
        # My logged hours by project
        context['my_hours'] = TimesheetEntry.objects.filter(
            timesheet__employee=employee,
            timesheet__status='approved'
        ).values('project__name', 'project__project_id').annotate(
            total_hours=models.Sum('hours')
        ).order_by('-total_hours')[:10]
    
    # Admin view
    if can_manage_projects(request.user):
        context['all_projects'] = Project.objects.select_related(
            'project_manager', 'department'
        ).order_by('-created_at')[:20]
        context['active_projects'] = Project.objects.filter(status='active').count()
    
    return render(request, 'hr_portal/project/dashboard.html', context)


@hr_portal_required
def project_list(request):
    """List all projects"""
    status = request.GET.get('status')
    department_id = request.GET.get('department')
    
    projects = Project.objects.select_related('project_manager', 'department')
    
    if status:
        projects = projects.filter(status=status)
    if department_id:
        projects = projects.filter(department_id=department_id)
    
    context = {
        'title': 'All Projects',
        'projects': projects.order_by('-created_at'),
        'status_choices': Project.STATUS_CHOICES,
        'departments': Department.objects.filter(is_active=True),
        'selected_status': status,
        'selected_department': department_id,
    }
    
    return render(request, 'hr_portal/project/list.html', context)


@hr_admin_required
def project_create(request):
    """Create a new project"""
    if request.method == 'POST':
        try:
            project_data = {
                'project_id': request.POST.get('project_id'),
                'name': request.POST.get('name'),
                'description': request.POST.get('description', ''),
                'client': request.POST.get('client', ''),
                'start_date': datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date(),
                'status': request.POST.get('status', 'planning'),
                'is_billable': request.POST.get('is_billable') == 'on',
                'created_by': request.user,
            }
            
            if request.POST.get('end_date'):
                project_data['end_date'] = datetime.strptime(
                    request.POST.get('end_date'), '%Y-%m-%d'
                ).date()
            
            if request.POST.get('budget_hours'):
                project_data['budget_hours'] = Decimal(request.POST.get('budget_hours'))
            
            if request.POST.get('budget_amount'):
                project_data['budget_amount'] = Decimal(request.POST.get('budget_amount'))
            
            if request.POST.get('project_manager'):
                project_data['project_manager'] = get_object_or_404(
                    Employee, id=request.POST.get('project_manager')
                )
            
            if request.POST.get('department'):
                project_data['department'] = get_object_or_404(
                    Department, id=request.POST.get('department')
                )
            
            project = Project.objects.create(**project_data)
            AuditService.log_project_action('create', project, request.user, request=request)
            messages.success(request, f'Project {project.project_id} created successfully.')
            return redirect('hr_portal:project_detail', project_id=project.project_id)
        
        except Exception as e:
            messages.error(request, f'Error creating project: {str(e)}')
    
    context = {
        'title': 'Create Project',
        'status_choices': Project.STATUS_CHOICES,
        'departments': Department.objects.filter(is_active=True),
        'managers': Employee.objects.filter(employment_status='active'),
    }
    
    return render(request, 'hr_portal/project/create.html', context)


@hr_portal_required
def project_detail(request, project_id):
    """View project details"""
    project = get_object_or_404(Project, project_id=project_id)
    employee = get_employee(request.user)
    
    # Check if user is assigned to project or is admin
    is_assigned = ProjectAssignment.objects.filter(
        project=project, employee=employee, is_active=True
    ).exists() if employee else False
    
    can_view = is_assigned or can_manage_projects(request.user)
    
    if not can_view:
        messages.error(request, 'You do not have permission to view this project.')
        return redirect('hr_portal:project_dashboard')
    
    # Get team members
    team_members = ProjectAssignment.objects.filter(
        project=project, is_active=True
    ).select_related('employee')
    
    # Get time logged
    from django.db.models import Sum
    time_logged = TimesheetEntry.objects.filter(
        project=project,
        timesheet__status='approved'
    ).aggregate(total=Sum('hours'))['total'] or Decimal('0')
    
    context = {
        'title': f'Project - {project.name}',
        'project': project,
        'team_members': team_members,
        'time_logged': time_logged,
        'can_manage': can_manage_projects(request.user),
        'is_assigned': is_assigned,
    }
    
    return render(request, 'hr_portal/project/detail.html', context)


@hr_admin_required
@require_POST
def project_add_member(request, project_id):
    """Add team member to project"""
    project = get_object_or_404(Project, project_id=project_id)
    
    try:
        employee = get_object_or_404(Employee, id=request.POST.get('employee_id'))
        role = request.POST.get('role', 'member')
        allocation = int(request.POST.get('allocation', 100))
        start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
        
        end_date = None
        if request.POST.get('end_date'):
            end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()
        
        ProjectAssignment.objects.create(
            project=project,
            employee=employee,
            role=role,
            allocation_percentage=allocation,
            start_date=start_date,
            end_date=end_date
        )
        
        messages.success(request, f'{employee.full_name} added to project.')
    except Exception as e:
        messages.error(request, f'Error adding team member: {str(e)}')
    
    return redirect('hr_portal:project_detail', project_id=project_id)


@hr_admin_required
@require_POST
def project_remove_member(request, project_id, assignment_id):
    """Remove team member from project"""
    assignment = get_object_or_404(ProjectAssignment, id=assignment_id, project__project_id=project_id)
    
    assignment.is_active = False
    assignment.end_date = timezone.now().date()
    assignment.save()
    
    messages.success(request, f'{assignment.employee.full_name} removed from project.')
    return redirect('hr_portal:project_detail', project_id=project_id)


@hr_portal_required
def project_timesheet_report(request, project_id):
    """View timesheet report for a project"""
    project = get_object_or_404(Project, project_id=project_id)
    employee = get_employee(request.user)
    
    # Check permissions
    is_assigned = ProjectAssignment.objects.filter(
        project=project, employee=employee, is_active=True
    ).exists() if employee else False
    
    if not (is_assigned or can_manage_projects(request.user)):
        messages.error(request, 'You do not have permission to view this report.')
        return redirect('hr_portal:project_dashboard')
    
    # Get time entries
    from django.db.models import Sum
    entries = TimesheetEntry.objects.filter(
        project=project,
        timesheet__status='approved'
    ).select_related('timesheet__employee').order_by('-date')
    
    # Summary by employee
    by_employee = entries.values(
        'timesheet__employee__employee_id',
        'timesheet__employee__user__first_name',
        'timesheet__employee__user__last_name'
    ).annotate(total_hours=Sum('hours')).order_by('-total_hours')
    
    context = {
        'title': f'Timesheet Report - {project.name}',
        'project': project,
        'entries': entries[:100],
        'by_employee': by_employee,
        'total_hours': project.total_logged_hours,
    }
    
    return render(request, 'hr_portal/project/timesheet_report.html', context)


# Import models for aggregation
from django.db import models
