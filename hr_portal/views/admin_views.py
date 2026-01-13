"""
Admin Views - HR Admin management views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils import timezone

from ..permissions import (
    hr_portal_required, hr_admin_required, app_admin_required,
    get_employee, is_app_admin
)
from ..models import (
    Employee, Department, Designation, HRRole, LeaveType, LeaveBalance,
    ExpenseCategory, AssetCategory, HolidayCalendar, AuditLog
)
from ..services import AuditService


@hr_admin_required
def admin_dashboard(request):
    """HR Admin dashboard"""
    context = {
        'title': 'HR Administration',
        'employee_count': Employee.objects.filter(employment_status='active').count(),
        'department_count': Department.objects.filter(is_active=True).count(),
        'pending_leaves': LeaveRequest.objects.filter(status='manager_approved').count(),
        'pending_expenses': ExpenseRequest.objects.filter(status='manager_approved').count(),
    }
    
    return render(request, 'hr_portal/admin/dashboard.html', context)


@app_admin_required
def user_management(request):
    """User and role management"""
    users = User.objects.select_related('hr_role', 'employee_profile').order_by('username')
    
    context = {
        'title': 'User Management',
        'users': users,
        'role_choices': HRRole.ROLE_TYPE_CHOICES,
    }
    
    return render(request, 'hr_portal/admin/users.html', context)


@app_admin_required
@require_POST
def assign_hr_role(request, user_id):
    """Assign HR role to user"""
    user = get_object_or_404(User, id=user_id)
    role_type = request.POST.get('role_type', 'employee')
    is_employee = request.POST.get('is_employee') == 'on'
    
    hr_role, created = HRRole.objects.get_or_create(user=user)
    hr_role.role_type = role_type
    hr_role.is_employee = is_employee
    hr_role.created_by = request.user
    hr_role.save()
    
    AuditService.log_action(
        'update', 'employee', str(user.id),
        f'HR Role assigned: {role_type}',
        request.user, request=request
    )
    
    messages.success(request, f'Role assigned to {user.username}.')
    return redirect('hr_portal:user_management')


# Import models for counts
from ..models import LeaveRequest, ExpenseRequest
