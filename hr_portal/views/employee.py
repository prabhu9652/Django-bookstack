"""
Employee Views - Employee management
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from ..permissions import (
    hr_portal_required, hr_admin_required, app_admin_required,
    get_employee, can_manage_employees
)
from ..models import Employee, Department, Designation, HRRole
from ..services import EmployeeService, AuditService


@hr_portal_required
def employee_list(request):
    """List all employees (HR admin view)"""
    if not can_manage_employees(request.user):
        messages.error(request, 'You do not have permission to view all employees.')
        return redirect('hr_portal:dashboard')
    
    employees = Employee.objects.select_related(
        'user', 'department', 'designation', 'reporting_manager'
    ).order_by('employee_id')
    
    # Filters
    department_id = request.GET.get('department')
    status = request.GET.get('status')
    search = request.GET.get('search')
    
    if department_id:
        employees = employees.filter(department_id=department_id)
    
    if status:
        employees = employees.filter(employment_status=status)
    
    if search:
        from django.db.models import Q
        employees = employees.filter(
            Q(employee_id__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search)
        )
    
    context = {
        'title': 'Employees',
        'employees': employees,
        'departments': Department.objects.filter(is_active=True),
        'status_choices': Employee.EMPLOYMENT_STATUS_CHOICES,
        'selected_department': department_id,
        'selected_status': status,
        'search_query': search,
    }
    
    return render(request, 'hr_portal/employee/list.html', context)


@hr_portal_required
def employee_detail(request, employee_id):
    """View employee details"""
    employee = get_object_or_404(Employee, employee_id=employee_id)
    current_employee = get_employee(request.user)
    
    # Check permissions
    can_view = (
        can_manage_employees(request.user) or
        employee == current_employee or
        (current_employee and employee.reporting_manager == current_employee)
    )
    
    if not can_view:
        messages.error(request, 'You do not have permission to view this employee.')
        return redirect('hr_portal:dashboard')
    
    context = {
        'title': f'Employee - {employee.full_name}',
        'employee': employee,
        'reporting_chain': employee.get_reporting_chain(),
        'direct_reports': employee.direct_reports.filter(employment_status='active'),
        'assigned_assets': employee.assigned_assets.select_related('category'),
        'can_edit': can_manage_employees(request.user),
    }
    
    return render(request, 'hr_portal/employee/detail.html', context)


@hr_admin_required
def employee_create(request):
    """Create a new employee"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Get or create user
                user_id = request.POST.get('user_id')
                if user_id:
                    user = get_object_or_404(User, id=user_id)
                else:
                    # Create new user
                    username = request.POST.get('username')
                    email = request.POST.get('email')
                    first_name = request.POST.get('first_name')
                    last_name = request.POST.get('last_name')
                    
                    if User.objects.filter(username=username).exists():
                        raise ValueError(f"Username '{username}' already exists")
                    
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=User.objects.make_random_password()
                    )
                
                # Create employee
                employee_data = {
                    'department': get_object_or_404(Department, id=request.POST.get('department')),
                    'designation': get_object_or_404(Designation, id=request.POST.get('designation')),
                    'joining_date': request.POST.get('joining_date'),
                    'employment_type': request.POST.get('employment_type', 'full_time'),
                    'work_location': request.POST.get('work_location', ''),
                    'phone': request.POST.get('phone', ''),
                    'address': request.POST.get('address', ''),
                }
                
                reporting_manager_id = request.POST.get('reporting_manager')
                if reporting_manager_id:
                    employee_data['reporting_manager'] = get_object_or_404(
                        Employee, id=reporting_manager_id
                    )
                
                employee = EmployeeService.create_employee(
                    user=user,
                    employee_data=employee_data,
                    created_by=request.user
                )
                
                # Log action
                AuditService.log_employee_action(
                    action='create',
                    employee=employee,
                    performed_by=request.user,
                    request=request
                )
                
                messages.success(request, f'Employee {employee.employee_id} created successfully.')
                return redirect('hr_portal:employee_detail', employee_id=employee.employee_id)
        
        except Exception as e:
            messages.error(request, f'Error creating employee: {str(e)}')
    
    # Get users without employee profiles
    users_without_profile = User.objects.filter(
        employee_profile__isnull=True,
        is_superuser=False
    )
    
    context = {
        'title': 'Create Employee',
        'departments': Department.objects.filter(is_active=True),
        'designations': Designation.objects.filter(is_active=True),
        'managers': Employee.objects.filter(employment_status='active'),
        'users_without_profile': users_without_profile,
        'employment_types': Employee.EMPLOYMENT_TYPE_CHOICES,
    }
    
    return render(request, 'hr_portal/employee/create.html', context)


@hr_admin_required
def employee_edit(request, employee_id):
    """Edit employee details"""
    employee = get_object_or_404(Employee, employee_id=employee_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Update user info
                employee.user.first_name = request.POST.get('first_name', '')
                employee.user.last_name = request.POST.get('last_name', '')
                employee.user.email = request.POST.get('email', '')
                employee.user.save()
                
                # Update employee info
                employee.department = get_object_or_404(Department, id=request.POST.get('department'))
                employee.designation = get_object_or_404(Designation, id=request.POST.get('designation'))
                employee.employment_type = request.POST.get('employment_type')
                employee.employment_status = request.POST.get('employment_status')
                employee.work_location = request.POST.get('work_location', '')
                employee.phone = request.POST.get('phone', '')
                employee.address = request.POST.get('address', '')
                
                reporting_manager_id = request.POST.get('reporting_manager')
                if reporting_manager_id:
                    employee.reporting_manager = get_object_or_404(Employee, id=reporting_manager_id)
                else:
                    employee.reporting_manager = None
                
                employee.save()
                
                # Log action
                AuditService.log_employee_action(
                    action='update',
                    employee=employee,
                    performed_by=request.user,
                    request=request
                )
                
                messages.success(request, 'Employee updated successfully.')
                return redirect('hr_portal:employee_detail', employee_id=employee.employee_id)
        
        except Exception as e:
            messages.error(request, f'Error updating employee: {str(e)}')
    
    context = {
        'title': f'Edit Employee - {employee.full_name}',
        'employee': employee,
        'departments': Department.objects.filter(is_active=True),
        'designations': Designation.objects.filter(is_active=True),
        'managers': Employee.objects.filter(employment_status='active').exclude(id=employee.id),
        'employment_types': Employee.EMPLOYMENT_TYPE_CHOICES,
        'employment_statuses': Employee.EMPLOYMENT_STATUS_CHOICES,
    }
    
    return render(request, 'hr_portal/employee/edit.html', context)


@hr_portal_required
def my_team(request):
    """View team members (for managers)"""
    employee = get_employee(request.user)
    
    if not employee or not employee.is_manager:
        messages.info(request, 'You do not have any direct reports.')
        return redirect('hr_portal:dashboard')
    
    team_members = EmployeeService.get_team_members(employee)
    
    context = {
        'title': 'My Team',
        'team_members': team_members,
    }
    
    return render(request, 'hr_portal/employee/team.html', context)


@hr_portal_required
def organization_chart(request):
    """View organization chart"""
    # Get top-level employees (no reporting manager)
    top_level = Employee.objects.filter(
        reporting_manager__isnull=True,
        employment_status='active'
    ).select_related('department', 'designation')
    
    context = {
        'title': 'Organization Chart',
        'top_level_employees': top_level,
    }
    
    return render(request, 'hr_portal/employee/org_chart.html', context)


# API endpoints for AJAX
@hr_portal_required
def api_get_designations(request, department_id):
    """Get designations for a department"""
    designations = Designation.objects.filter(
        department_id=department_id,
        is_active=True
    ).values('id', 'title')
    
    return JsonResponse({'designations': list(designations)})


@hr_portal_required
def api_search_employees(request):
    """Search employees (for autocomplete)"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'employees': []})
    
    from django.db.models import Q
    employees = Employee.objects.filter(
        Q(employee_id__icontains=query) |
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query),
        employment_status='active'
    ).select_related('user')[:10]
    
    results = [{
        'id': e.id,
        'employee_id': e.employee_id,
        'name': e.full_name,
        'department': e.department.name,
    } for e in employees]
    
    return JsonResponse({'employees': results})
