"""
Employee Service - Business logic for employee management
"""

from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Employee, Department, Designation, HRRole, LeaveBalance, LeaveType


class EmployeeService:
    """Service class for employee-related operations"""

    @staticmethod
    @transaction.atomic
    def create_employee(user, employee_data, created_by=None):
        """
        Create a new employee record and associated HR role.
        
        Args:
            user: Django User instance
            employee_data: dict with employee fields
            created_by: User who is creating this employee
        
        Returns:
            Employee instance
        """
        # Generate employee ID
        last_employee = Employee.objects.order_by('-id').first()
        next_id = (last_employee.id + 1) if last_employee else 1
        employee_id = f"EMP{next_id:04d}"
        
        # Create employee
        employee = Employee.objects.create(
            user=user,
            employee_id=employee_id,
            department=employee_data['department'],
            designation=employee_data['designation'],
            joining_date=employee_data.get('joining_date', timezone.now().date()),
            employment_type=employee_data.get('employment_type', 'full_time'),
            employment_status='active',
            reporting_manager=employee_data.get('reporting_manager'),
            work_location=employee_data.get('work_location', ''),
            phone=employee_data.get('phone', ''),
            address=employee_data.get('address', ''),
            created_by=created_by,
        )
        
        # Create or update HR role
        hr_role, _ = HRRole.objects.get_or_create(user=user)
        hr_role.is_employee = True
        hr_role.can_access_hr_portal = True
        hr_role.save()
        
        # Initialize leave balances for current year
        EmployeeService.initialize_leave_balances(employee)
        
        return employee

    @staticmethod
    def initialize_leave_balances(employee, year=None):
        """Initialize leave balances for an employee"""
        if year is None:
            year = timezone.now().year
        
        leave_types = LeaveType.objects.filter(is_active=True)
        for leave_type in leave_types:
            LeaveBalance.objects.get_or_create(
                employee=employee,
                leave_type=leave_type,
                year=year,
                defaults={'allocated_days': leave_type.default_days}
            )

    @staticmethod
    def get_team_members(manager):
        """Get all direct reports for a manager"""
        return Employee.objects.filter(
            reporting_manager=manager,
            employment_status='active'
        ).select_related('user', 'department', 'designation')

    @staticmethod
    def get_department_employees(department):
        """Get all employees in a department"""
        return Employee.objects.filter(
            department=department,
            employment_status='active'
        ).select_related('user', 'designation', 'reporting_manager')

    @staticmethod
    def search_employees(query, department=None, status=None):
        """Search employees by name, ID, or email"""
        employees = Employee.objects.select_related('user', 'department', 'designation')
        
        if query:
            employees = employees.filter(
                models.Q(employee_id__icontains=query) |
                models.Q(user__first_name__icontains=query) |
                models.Q(user__last_name__icontains=query) |
                models.Q(user__email__icontains=query)
            )
        
        if department:
            employees = employees.filter(department=department)
        
        if status:
            employees = employees.filter(employment_status=status)
        
        return employees

    @staticmethod
    def get_employee_dashboard_data(employee):
        """Get dashboard data for an employee"""
        from ..models import LeaveRequest, ExpenseRequest, Timesheet, Asset
        
        current_year = timezone.now().year
        
        return {
            'leave_balances': employee.leave_balances.filter(year=current_year),
            'pending_leaves': LeaveRequest.objects.filter(
                employee=employee, status__in=['pending', 'manager_approved']
            ).count(),
            'pending_expenses': ExpenseRequest.objects.filter(
                employee=employee, status__in=['submitted', 'manager_approved']
            ).count(),
            'assigned_assets': Asset.objects.filter(assigned_to=employee).count(),
            'recent_leaves': LeaveRequest.objects.filter(employee=employee)[:5],
            'recent_expenses': ExpenseRequest.objects.filter(employee=employee)[:5],
        }

    @staticmethod
    def terminate_employee(employee, termination_date, terminated_by):
        """Handle employee termination"""
        employee.employment_status = 'terminated'
        employee.termination_date = termination_date
        employee.save()
        
        # Update HR role
        if hasattr(employee.user, 'hr_role'):
            employee.user.hr_role.can_access_hr_portal = False
            employee.user.hr_role.save()
        
        # Return all assigned assets
        from .asset_service import AssetService
        for asset in employee.assigned_assets.all():
            AssetService.return_asset(asset, terminated_by)
