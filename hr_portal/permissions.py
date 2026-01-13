"""
HR Portal Permissions - Role-based access control

This module provides decorators and utilities for enforcing
role-based access control in the HR Portal.

Enterprise-grade implementation with:
- Admin-controlled feature toggles
- Per-user access control
- Immediate effect on access changes
- Both frontend visibility and backend authorization
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)


def get_hr_role(user):
    """
    Get HR role for a user.
    
    Returns None if user is not authenticated or has no HR role.
    Does NOT auto-create roles - admin must explicitly grant access.
    """
    if not user.is_authenticated:
        return None
    
    # Import here to avoid circular imports
    from .models import HRRole
    
    try:
        return user.hr_role
    except HRRole.DoesNotExist:
        return None


def get_employee(user):
    """Get employee profile for a user"""
    if not user.is_authenticated:
        return None
    
    # Import here to avoid circular imports
    from .models import Employee
    
    try:
        return user.employee_profile
    except Employee.DoesNotExist:
        return None


def is_employee(user):
    """Check if user is marked as an employee"""
    hr_role = get_hr_role(user)
    return hr_role and hr_role.is_employee


def can_access_hr_portal(user):
    """
    Check if user can access HR portal.
    
    This is the PRIMARY gate for HR Portal access.
    Access is controlled by:
    1. Superuser status (always has access)
    2. HRRole.can_access_hr_portal flag (admin-controlled)
    
    Changes to this flag take effect immediately - no restart required.
    """
    if not user.is_authenticated:
        return False
    
    # Superusers always have access
    if user.is_superuser:
        return True
    
    # Check the admin-controlled access flag
    hr_role = get_hr_role(user)
    if hr_role is None:
        # No HR role assigned = no access
        return False
    
    # The can_access_hr_portal flag is the definitive gate
    return hr_role.can_access_hr_portal


def is_hr_portal_enabled_for_user(user):
    """
    Alias for can_access_hr_portal - used for clarity in templates.
    
    This function name makes it clear this is an admin-controlled toggle.
    """
    return can_access_hr_portal(user)


def is_hr_admin(user):
    """Check if user is HR admin"""
    if user.is_superuser:
        return True
    hr_role = get_hr_role(user)
    return hr_role and hr_role.role_type in ['app_admin', 'hr_admin']


def is_finance_admin(user):
    """Check if user is finance admin"""
    if user.is_superuser:
        return True
    hr_role = get_hr_role(user)
    return hr_role and hr_role.role_type in ['app_admin', 'finance_admin']


def is_app_admin(user):
    """Check if user is app admin"""
    if user.is_superuser:
        return True
    hr_role = get_hr_role(user)
    return hr_role and hr_role.role_type == 'app_admin'


def is_manager(user):
    """Check if user is a manager (has direct reports)"""
    employee = get_employee(user)
    return employee and employee.is_manager


def can_manage_employees(user):
    """Check if user can manage employees"""
    if user.is_superuser:
        return True
    hr_role = get_hr_role(user)
    return hr_role and hr_role.can_manage_employees


def can_manage_leaves(user):
    """Check if user can manage leaves"""
    if user.is_superuser:
        return True
    hr_role = get_hr_role(user)
    return hr_role and hr_role.can_manage_leaves


def can_manage_expenses(user):
    """Check if user can manage expenses"""
    if user.is_superuser:
        return True
    hr_role = get_hr_role(user)
    return hr_role and hr_role.can_manage_expenses


def can_manage_assets(user):
    """Check if user can manage assets"""
    if user.is_superuser:
        return True
    hr_role = get_hr_role(user)
    return hr_role and hr_role.can_manage_assets


def can_manage_timesheets(user):
    """Check if user can manage timesheets"""
    if user.is_superuser:
        return True
    hr_role = get_hr_role(user)
    return hr_role and hr_role.can_manage_timesheets


def can_manage_projects(user):
    """Check if user can manage projects"""
    if user.is_superuser:
        return True
    hr_role = get_hr_role(user)
    return hr_role and hr_role.can_manage_projects


def can_view_reports(user):
    """Check if user can view reports"""
    if user.is_superuser:
        return True
    hr_role = get_hr_role(user)
    return hr_role and hr_role.can_view_reports


# =============================================================================
# DECORATORS
# =============================================================================

def hr_portal_required(view_func):
    """
    Decorator to require HR portal access.
    
    This is the primary security gate for all HR Portal views.
    It checks the admin-controlled can_access_hr_portal flag.
    
    Unauthorized access attempts are:
    - Logged for security auditing
    - Redirected with appropriate error message
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access the HR Portal.')
            return redirect('accounts.login')
        
        if not can_access_hr_portal(request.user):
            # Log unauthorized access attempt
            logger.warning(
                f'HR Portal access denied for user {request.user.username} '
                f'(IP: {request.META.get("REMOTE_ADDR", "unknown")})'
            )
            messages.error(
                request, 
                'You do not have access to the HR Portal. '
                'Please contact your administrator if you believe this is an error.'
            )
            return redirect('home.index')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def employee_required(view_func):
    """Decorator to require employee status"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('accounts.login')
        
        if not is_employee(request.user):
            messages.error(request, 'You must be an employee to access this page.')
            return redirect('home.index')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def hr_admin_required(view_func):
    """Decorator to require HR admin role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('accounts.login')
        
        # First check HR portal access
        if not can_access_hr_portal(request.user):
            messages.error(request, 'You do not have access to the HR Portal.')
            return redirect('home.index')
        
        if not is_hr_admin(request.user):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('hr_portal:dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def finance_admin_required(view_func):
    """Decorator to require finance admin role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('accounts.login')
        
        # First check HR portal access
        if not can_access_hr_portal(request.user):
            messages.error(request, 'You do not have access to the HR Portal.')
            return redirect('home.index')
        
        if not is_finance_admin(request.user):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('hr_portal:dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def app_admin_required(view_func):
    """Decorator to require app admin role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('accounts.login')
        
        # First check HR portal access
        if not can_access_hr_portal(request.user):
            messages.error(request, 'You do not have access to the HR Portal.')
            return redirect('home.index')
        
        if not is_app_admin(request.user):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('hr_portal:dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def manager_required(view_func):
    """Decorator to require manager status"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('accounts.login')
        
        # First check HR portal access
        if not can_access_hr_portal(request.user):
            messages.error(request, 'You do not have access to the HR Portal.')
            return redirect('home.index')
        
        if not is_manager(request.user) and not is_hr_admin(request.user):
            messages.error(request, 'You must be a manager to access this page.')
            return redirect('hr_portal:dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


# =============================================================================
# CONTEXT PROCESSOR
# =============================================================================

def hr_portal_context(request):
    """
    Context processor for HR portal permissions.
    
    Provides template variables for:
    - Navigation visibility (can_access_hr_portal)
    - Role-based UI elements
    - Permission checks
    
    All checks are performed against the database on each request,
    ensuring admin changes take effect immediately.
    """
    if not request.user.is_authenticated:
        return {
            'can_access_hr_portal': False,
            'hr_portal_enabled': False,
            'is_employee': False,
            'is_hr_admin': False,
            'is_finance_admin': False,
            'is_app_admin': False,
            'is_manager': False,
            'can_manage_employees': False,
            'can_manage_leaves': False,
            'can_manage_expenses': False,
            'can_manage_assets': False,
            'can_manage_timesheets': False,
            'can_manage_projects': False,
            'can_view_reports': False,
        }
    
    # Get HR role once for efficiency
    hr_role = get_hr_role(request.user)
    has_portal_access = can_access_hr_portal(request.user)
    
    return {
        # Primary access control - used for navigation visibility
        'can_access_hr_portal': has_portal_access,
        'hr_portal_enabled': has_portal_access,  # Alias for clarity
        
        # Role checks
        'is_employee': is_employee(request.user),
        'is_hr_admin': is_hr_admin(request.user),
        'is_finance_admin': is_finance_admin(request.user),
        'is_app_admin': is_app_admin(request.user),
        'is_manager': is_manager(request.user),
        
        # Granular permissions
        'can_manage_employees': can_manage_employees(request.user),
        'can_manage_leaves': can_manage_leaves(request.user),
        'can_manage_expenses': can_manage_expenses(request.user),
        'can_manage_assets': can_manage_assets(request.user),
        'can_manage_timesheets': can_manage_timesheets(request.user),
        'can_manage_projects': can_manage_projects(request.user),
        'can_view_reports': can_view_reports(request.user),
        
        # HR Role object for advanced template logic
        'hr_role': hr_role,
    }
