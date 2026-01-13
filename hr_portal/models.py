"""
HR Portal Models - Enterprise-Grade HR Management System

This module contains all models for the HR Portal including:
- Employee Management
- Leave Management
- Expense Management
- Asset Management
- Timesheet Management
- Project Management
- Holiday Calendar
- Approval Workflows
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid


# =============================================================================
# CORE MODELS - Employee & Organization Structure
# =============================================================================

class Department(models.Model):
    """Company departments for organizational structure"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey(
        'Employee', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='headed_departments'
    )
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sub_departments'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.code} - {self.name}"


class Designation(models.Model):
    """Job titles/designations within the company"""
    title = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=1, help_text="Hierarchy level (1=Entry, 10=Executive)")
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='designations'
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['department', 'level', 'title']
        unique_together = ['title', 'department']

    def __str__(self):
        return f"{self.title} ({self.department.code})"


class Employee(models.Model):
    """
    Core Employee model - extends Django User with HR-specific fields.
    This is the central entity for all HR operations.
    """
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('intern', 'Intern'),
        ('consultant', 'Consultant'),
    ]
    
    EMPLOYMENT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('notice_period', 'Notice Period'),
        ('terminated', 'Terminated'),
        ('resigned', 'Resigned'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    # Link to Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True, help_text="Unique employee identifier (e.g., EMP001)")
    
    # Personal Information
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    personal_email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Employment Information
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='employees'
    )
    designation = models.ForeignKey(
        Designation, on_delete=models.PROTECT, related_name='employees'
    )
    reporting_manager = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='direct_reports'
    )
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time')
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, default='active')
    joining_date = models.DateField()
    confirmation_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    
    # Work Location
    work_location = models.CharField(max_length=100, blank=True, help_text="Office location or Remote")
    
    # Profile
    profile_photo = models.ImageField(upload_to='hr_portal/employee_photos/', null=True, blank=True)
    bio = models.TextField(blank=True, help_text="Short professional bio")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='created_employees'
    )

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        permissions = [
            ('view_all_employees', 'Can view all employees'),
            ('manage_employees', 'Can manage employee records'),
            ('view_team_employees', 'Can view team employees'),
        ]

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def is_manager(self):
        """Check if employee has direct reports"""
        return self.direct_reports.filter(employment_status='active').exists()

    def get_team_members(self):
        """Get all direct reports"""
        return Employee.objects.filter(reporting_manager=self, employment_status='active')

    def get_reporting_chain(self):
        """Get the full reporting chain up to top"""
        chain = []
        current = self.reporting_manager
        while current:
            chain.append(current)
            current = current.reporting_manager
        return chain


# =============================================================================
# HOLIDAY CALENDAR
# =============================================================================

class HolidayCalendar(models.Model):
    """Company holiday calendar with location-based holidays"""
    HOLIDAY_TYPE_CHOICES = [
        ('public', 'Public Holiday'),
        ('company', 'Company Holiday'),
        ('optional', 'Optional Holiday'),
        ('restricted', 'Restricted Holiday'),
    ]

    name = models.CharField(max_length=100)
    date = models.DateField()
    holiday_type = models.CharField(max_length=20, choices=HOLIDAY_TYPE_CHOICES, default='public')
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True, help_text="Leave blank for company-wide")
    is_active = models.BooleanField(default=True)
    year = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        unique_together = ['name', 'date', 'location']
        verbose_name = 'Holiday'
        verbose_name_plural = 'Holidays'

    def __str__(self):
        location_str = f" ({self.location})" if self.location else ""
        return f"{self.name} - {self.date}{location_str}"

    def save(self, *args, **kwargs):
        if not self.year:
            self.year = self.date.year
        super().save(*args, **kwargs)


# =============================================================================
# LEAVE MANAGEMENT
# =============================================================================

class LeaveType(models.Model):
    """Types of leave available to employees"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    default_days = models.PositiveIntegerField(default=0, help_text="Default annual allocation")
    is_paid = models.BooleanField(default=True)
    is_carry_forward = models.BooleanField(default=False, help_text="Can unused days be carried forward?")
    max_carry_forward_days = models.PositiveIntegerField(default=0)
    requires_approval = models.BooleanField(default=True)
    requires_document = models.BooleanField(default=False, help_text="Requires supporting document?")
    min_days_notice = models.PositiveIntegerField(default=0, help_text="Minimum days notice required")
    is_active = models.BooleanField(default=True)
    color = models.CharField(max_length=7, default='#3B82F6', help_text="Color for calendar display")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Leave Type'
        verbose_name_plural = 'Leave Types'

    def __str__(self):
        return f"{self.code} - {self.name}"


class LeaveBalance(models.Model):
    """Track leave balances for each employee per leave type per year"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='balances')
    year = models.PositiveIntegerField()
    allocated_days = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    used_days = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    carried_forward_days = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    adjusted_days = models.DecimalField(max_digits=5, decimal_places=1, default=0, help_text="Manual adjustments")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['employee', 'leave_type', 'year']
        ordering = ['employee', 'leave_type']
        verbose_name = 'Leave Balance'
        verbose_name_plural = 'Leave Balances'

    def __str__(self):
        return f"{self.employee.employee_id} - {self.leave_type.code} ({self.year})"

    @property
    def available_days(self):
        """Calculate available leave days"""
        return self.allocated_days + self.carried_forward_days + self.adjusted_days - self.used_days

    @property
    def total_entitled(self):
        """Total entitled days including carry forward"""
        return self.allocated_days + self.carried_forward_days + self.adjusted_days


class LeaveRequest(models.Model):
    """Employee leave requests with approval workflow"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('manager_approved', 'Manager Approved'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    DURATION_TYPE_CHOICES = [
        ('full_day', 'Full Day'),
        ('first_half', 'First Half'),
        ('second_half', 'Second Half'),
    ]

    # Request Details
    request_id = models.CharField(max_length=20, unique=True, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT, related_name='requests')
    
    # Leave Period
    start_date = models.DateField()
    end_date = models.DateField()
    duration_type = models.CharField(max_length=20, choices=DURATION_TYPE_CHOICES, default='full_day')
    total_days = models.DecimalField(max_digits=5, decimal_places=1)
    
    # Request Info
    reason = models.TextField()
    supporting_document = models.FileField(upload_to='hr_portal/leave_documents/', null=True, blank=True)
    contact_during_leave = models.CharField(max_length=100, blank=True)
    
    # Status & Workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Manager Approval
    manager_approved_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='manager_approved_leaves'
    )
    manager_approved_at = models.DateTimeField(null=True, blank=True)
    manager_comments = models.TextField(blank=True)
    
    # HR Approval
    hr_approved_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='hr_approved_leaves'
    )
    hr_approved_at = models.DateTimeField(null=True, blank=True)
    hr_comments = models.TextField(blank=True)
    
    # Rejection
    rejected_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='rejected_leaves'
    )
    rejected_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'
        permissions = [
            ('approve_leave_as_manager', 'Can approve leave as manager'),
            ('approve_leave_as_hr', 'Can approve leave as HR'),
            ('view_all_leaves', 'Can view all leave requests'),
            ('view_team_leaves', 'Can view team leave requests'),
        ]

    def __str__(self):
        return f"{self.request_id} - {self.employee.employee_id} ({self.leave_type.code})"

    def save(self, *args, **kwargs):
        if not self.request_id:
            self.request_id = f"LV{timezone.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def submit(self):
        """Submit leave request for approval"""
        self.status = 'pending'
        self.save()

    def approve_by_manager(self, manager, comments=''):
        """Manager approval"""
        self.status = 'manager_approved'
        self.manager_approved_by = manager
        self.manager_approved_at = timezone.now()
        self.manager_comments = comments
        self.save()

    def approve_by_hr(self, hr_admin, comments=''):
        """HR final approval - deducts leave balance"""
        self.status = 'approved'
        self.hr_approved_by = hr_admin
        self.hr_approved_at = timezone.now()
        self.hr_comments = comments
        self.save()
        
        # Deduct from leave balance
        balance, _ = LeaveBalance.objects.get_or_create(
            employee=self.employee,
            leave_type=self.leave_type,
            year=self.start_date.year,
            defaults={'allocated_days': self.leave_type.default_days}
        )
        balance.used_days += self.total_days
        balance.save()

    def reject(self, rejected_by, reason):
        """Reject leave request"""
        self.status = 'rejected'
        self.rejected_by = rejected_by
        self.rejected_at = timezone.now()
        self.rejection_reason = reason
        self.save()

    def cancel(self):
        """Cancel leave request"""
        if self.status == 'approved':
            # Restore leave balance
            try:
                balance = LeaveBalance.objects.get(
                    employee=self.employee,
                    leave_type=self.leave_type,
                    year=self.start_date.year
                )
                balance.used_days -= self.total_days
                balance.save()
            except LeaveBalance.DoesNotExist:
                pass
        self.status = 'cancelled'
        self.save()


# =============================================================================
# EXPENSE MANAGEMENT
# =============================================================================

class ExpenseCategory(models.Model):
    """Categories for expense claims"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                     help_text="Maximum claimable amount per request")
    requires_receipt = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Expense Category'
        verbose_name_plural = 'Expense Categories'

    def __str__(self):
        return f"{self.code} - {self.name}"


class ExpenseRequest(models.Model):
    """Employee expense claims with approval workflow"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('manager_approved', 'Manager Approved'),
        ('finance_approved', 'Finance Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('INR', 'Indian Rupee'),
        ('CAD', 'Canadian Dollar'),
        ('AUD', 'Australian Dollar'),
    ]

    # Request Details
    request_id = models.CharField(max_length=20, unique=True, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='expense_requests')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, related_name='requests')
    
    # Expense Details
    title = models.CharField(max_length=200)
    description = models.TextField()
    expense_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    receipt = models.FileField(upload_to='hr_portal/expense_receipts/', null=True, blank=True)
    
    # Project/Cost Center (optional)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    
    # Status & Workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Manager Approval
    manager_approved_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='manager_approved_expenses'
    )
    manager_approved_at = models.DateTimeField(null=True, blank=True)
    manager_comments = models.TextField(blank=True)
    
    # Finance Approval
    finance_approved_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='finance_approved_expenses'
    )
    finance_approved_at = models.DateTimeField(null=True, blank=True)
    finance_comments = models.TextField(blank=True)
    
    # Payment
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    
    # Rejection
    rejected_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='rejected_expenses'
    )
    rejected_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Expense Request'
        verbose_name_plural = 'Expense Requests'
        permissions = [
            ('approve_expense_as_manager', 'Can approve expense as manager'),
            ('approve_expense_as_finance', 'Can approve expense as finance'),
            ('mark_expense_paid', 'Can mark expense as paid'),
            ('view_all_expenses', 'Can view all expense requests'),
            ('view_team_expenses', 'Can view team expense requests'),
        ]

    def __str__(self):
        return f"{self.request_id} - {self.employee.employee_id} ({self.amount} {self.currency})"

    def save(self, *args, **kwargs):
        if not self.request_id:
            self.request_id = f"EX{timezone.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def submit(self):
        self.status = 'submitted'
        self.save()

    def approve_by_manager(self, manager, comments=''):
        self.status = 'manager_approved'
        self.manager_approved_by = manager
        self.manager_approved_at = timezone.now()
        self.manager_comments = comments
        self.save()

    def approve_by_finance(self, finance_admin, comments=''):
        self.status = 'finance_approved'
        self.finance_approved_by = finance_admin
        self.finance_approved_at = timezone.now()
        self.finance_comments = comments
        self.save()

    def mark_paid(self, payment_reference=''):
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.payment_reference = payment_reference
        self.save()

    def reject(self, rejected_by, reason):
        self.status = 'rejected'
        self.rejected_by = rejected_by
        self.rejected_at = timezone.now()
        self.rejection_reason = reason
        self.save()


# =============================================================================
# ASSET MANAGEMENT
# =============================================================================

class AssetCategory(models.Model):
    """Categories for company assets"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    depreciation_years = models.PositiveIntegerField(default=3, help_text="Years for depreciation")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Asset Category'
        verbose_name_plural = 'Asset Categories'

    def __str__(self):
        return f"{self.code} - {self.name}"


class Asset(models.Model):
    """Company asset inventory"""
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('damaged', 'Damaged'),
        ('disposed', 'Disposed'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]

    # Asset Details
    asset_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT, related_name='assets')
    description = models.TextField(blank=True)
    
    # Specifications
    serial_number = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    specifications = models.JSONField(default=dict, blank=True, help_text="Additional specs as JSON")
    
    # Financial
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    
    # Status
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    location = models.CharField(max_length=100, blank=True)
    
    # Current Assignment
    assigned_to = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_assets'
    )
    assigned_date = models.DateField(null=True, blank=True)
    
    # Metadata
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['asset_id']
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        permissions = [
            ('manage_assets', 'Can manage company assets'),
            ('assign_assets', 'Can assign assets to employees'),
            ('view_all_assets', 'Can view all assets'),
        ]

    def __str__(self):
        return f"{self.asset_id} - {self.name}"

    def assign_to_employee(self, employee, assigned_by=None):
        """Assign asset to an employee"""
        self.assigned_to = employee
        self.assigned_date = timezone.now().date()
        self.status = 'assigned'
        self.save()
        
        # Create assignment record
        AssetAssignment.objects.create(
            asset=self,
            employee=employee,
            assigned_by=assigned_by,
            assignment_type='assigned'
        )

    def return_asset(self, returned_by=None, condition='good', notes=''):
        """Return asset from employee"""
        if self.assigned_to:
            # Close current assignment
            current_assignment = AssetAssignment.objects.filter(
                asset=self, employee=self.assigned_to, returned_date__isnull=True
            ).first()
            if current_assignment:
                current_assignment.returned_date = timezone.now().date()
                current_assignment.return_condition = condition
                current_assignment.return_notes = notes
                current_assignment.save()
        
        self.assigned_to = None
        self.assigned_date = None
        self.status = 'available'
        self.condition = condition
        self.save()


class AssetAssignment(models.Model):
    """Track asset assignment history"""
    ASSIGNMENT_TYPE_CHOICES = [
        ('assigned', 'Assigned'),
        ('transferred', 'Transferred'),
        ('temporary', 'Temporary'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='assignments')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='asset_assignments')
    assigned_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assets_assigned_by'
    )
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPE_CHOICES, default='assigned')
    assigned_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)
    return_condition = models.CharField(max_length=20, blank=True)
    return_notes = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-assigned_date']
        verbose_name = 'Asset Assignment'
        verbose_name_plural = 'Asset Assignments'

    def __str__(self):
        return f"{self.asset.asset_id} -> {self.employee.employee_id}"


# =============================================================================
# PROJECT MANAGEMENT (HR-Level)
# =============================================================================

class Project(models.Model):
    """Projects for timesheet and expense tracking"""
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    project_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client = models.CharField(max_length=200, blank=True)
    
    # Project Details
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    
    # Budget
    budget_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Team
    project_manager = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='managed_projects'
    )
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='projects'
    )
    
    # Metadata
    is_billable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        permissions = [
            ('manage_projects', 'Can manage projects'),
            ('view_all_projects', 'Can view all projects'),
        ]

    def __str__(self):
        return f"{self.project_id} - {self.name}"

    @property
    def total_logged_hours(self):
        """Get total hours logged on this project"""
        from django.db.models import Sum
        result = self.timesheet_entries.aggregate(total=Sum('hours'))
        return result['total'] or Decimal('0')


class ProjectAssignment(models.Model):
    """Employee assignment to projects"""
    ROLE_CHOICES = [
        ('member', 'Team Member'),
        ('lead', 'Team Lead'),
        ('manager', 'Project Manager'),
        ('consultant', 'Consultant'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='assignments')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='project_assignments')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    allocation_percentage = models.PositiveIntegerField(
        default=100, validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Percentage of time allocated to this project"
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['project', 'employee']
        unique_together = ['project', 'employee']
        verbose_name = 'Project Assignment'
        verbose_name_plural = 'Project Assignments'

    def __str__(self):
        return f"{self.employee.employee_id} on {self.project.project_id}"


# =============================================================================
# TIMESHEET MANAGEMENT
# =============================================================================

class Timesheet(models.Model):
    """Weekly timesheet for employees"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='timesheets')
    week_start_date = models.DateField(help_text="Monday of the week")
    week_end_date = models.DateField(help_text="Sunday of the week")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Totals (calculated)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Approval
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='approved_timesheets'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_comments = models.TextField(blank=True)
    
    # Rejection
    rejected_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='rejected_timesheets'
    )
    rejected_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Metadata
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-week_start_date']
        unique_together = ['employee', 'week_start_date']
        verbose_name = 'Timesheet'
        verbose_name_plural = 'Timesheets'
        permissions = [
            ('approve_timesheet', 'Can approve timesheets'),
            ('view_all_timesheets', 'Can view all timesheets'),
            ('view_team_timesheets', 'Can view team timesheets'),
        ]

    def __str__(self):
        return f"{self.employee.employee_id} - Week of {self.week_start_date}"

    def calculate_total_hours(self):
        """Calculate total hours from entries"""
        from django.db.models import Sum
        result = self.entries.aggregate(total=Sum('hours'))
        self.total_hours = result['total'] or Decimal('0')
        self.save(update_fields=['total_hours'])

    def submit(self):
        self.calculate_total_hours()
        self.status = 'submitted'
        self.submitted_at = timezone.now()
        self.save()

    def approve(self, approved_by, comments=''):
        self.status = 'approved'
        self.approved_by = approved_by
        self.approved_at = timezone.now()
        self.approval_comments = comments
        self.is_locked = True
        self.save()

    def reject(self, rejected_by, reason):
        self.status = 'rejected'
        self.rejected_by = rejected_by
        self.rejected_at = timezone.now()
        self.rejection_reason = reason
        self.save()


class TimesheetEntry(models.Model):
    """Individual timesheet entries (daily/project-based)"""
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE, related_name='entries')
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='timesheet_entries')
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.25')), MaxValueValidator(Decimal('24'))
    ])
    description = models.TextField(blank=True, help_text="Work description for this entry")
    is_billable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'project']
        verbose_name = 'Timesheet Entry'
        verbose_name_plural = 'Timesheet Entries'

    def __str__(self):
        return f"{self.timesheet.employee.employee_id} - {self.project.project_id} - {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update timesheet total
        self.timesheet.calculate_total_hours()


# =============================================================================
# APPROVAL WORKFLOW & AUDIT
# =============================================================================

class ApprovalWorkflow(models.Model):
    """Define approval workflows for different request types"""
    REQUEST_TYPE_CHOICES = [
        ('leave', 'Leave Request'),
        ('expense', 'Expense Request'),
        ('timesheet', 'Timesheet'),
        ('asset', 'Asset Request'),
    ]

    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    requires_manager_approval = models.BooleanField(default=True)
    requires_hr_approval = models.BooleanField(default=True)
    requires_finance_approval = models.BooleanField(default=False)
    auto_approve_threshold = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Auto-approve if amount/days below this threshold"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Approval Workflow'
        verbose_name_plural = 'Approval Workflows'

    def __str__(self):
        return f"{self.name} ({self.request_type})"


class AuditLog(models.Model):
    """Comprehensive audit trail for all HR actions"""
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('submit', 'Submitted'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('cancel', 'Cancelled'),
        ('assign', 'Assigned'),
        ('return', 'Returned'),
    ]
    
    ENTITY_TYPE_CHOICES = [
        ('employee', 'Employee'),
        ('leave_request', 'Leave Request'),
        ('expense_request', 'Expense Request'),
        ('timesheet', 'Timesheet'),
        ('asset', 'Asset'),
        ('project', 'Project'),
    ]

    # Action Details
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    entity_type = models.CharField(max_length=30, choices=ENTITY_TYPE_CHOICES)
    entity_id = models.CharField(max_length=50)
    entity_description = models.CharField(max_length=200, blank=True)
    
    # Actor
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='hr_audit_logs')
    performed_at = models.DateTimeField(auto_now_add=True)
    
    # Context
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Changes
    old_values = models.JSONField(default=dict, blank=True)
    new_values = models.JSONField(default=dict, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ['-performed_at']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['performed_by', 'performed_at']),
        ]

    def __str__(self):
        return f"{self.action} {self.entity_type} ({self.entity_id}) by {self.performed_by}"


# =============================================================================
# HR PORTAL ROLES & PERMISSIONS
# =============================================================================

class HRRole(models.Model):
    """Custom HR roles for fine-grained access control"""
    ROLE_TYPE_CHOICES = [
        ('app_admin', 'App Admin'),
        ('hr_admin', 'HR Admin'),
        ('finance_admin', 'Finance Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hr_role')
    role_type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICES, default='employee')
    is_employee = models.BooleanField(default=False, help_text="User is marked as an employee")
    can_access_hr_portal = models.BooleanField(default=False)
    
    # Specific Permissions
    can_manage_employees = models.BooleanField(default=False)
    can_manage_leaves = models.BooleanField(default=False)
    can_manage_expenses = models.BooleanField(default=False)
    can_manage_assets = models.BooleanField(default=False)
    can_manage_timesheets = models.BooleanField(default=False)
    can_manage_projects = models.BooleanField(default=False)
    can_manage_holidays = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='created_hr_roles'
    )

    class Meta:
        verbose_name = 'HR Role'
        verbose_name_plural = 'HR Roles'

    def __str__(self):
        return f"{self.user.username} - {self.get_role_type_display()}"

    def save(self, *args, **kwargs):
        """
        Auto-set permissions based on role type.
        
        Note: can_access_hr_portal is NOT auto-set for 'employee' role type.
        This allows admins to control portal access independently of role.
        For admin roles (app_admin, hr_admin, finance_admin, manager),
        access is auto-enabled as these roles require portal access.
        """
        # Track if this is a new record or role_type changed
        is_new = self.pk is None
        
        if self.role_type == 'app_admin':
            self.is_employee = True
            self.can_access_hr_portal = True
            self.can_manage_employees = True
            self.can_manage_leaves = True
            self.can_manage_expenses = True
            self.can_manage_assets = True
            self.can_manage_timesheets = True
            self.can_manage_projects = True
            self.can_manage_holidays = True
            self.can_view_reports = True
        elif self.role_type == 'hr_admin':
            self.is_employee = True
            self.can_access_hr_portal = True
            self.can_manage_employees = True
            self.can_manage_leaves = True
            self.can_manage_assets = True
            self.can_manage_holidays = True
            self.can_view_reports = True
        elif self.role_type == 'finance_admin':
            self.is_employee = True
            self.can_access_hr_portal = True
            self.can_manage_expenses = True
            self.can_view_reports = True
        elif self.role_type == 'manager':
            self.is_employee = True
            self.can_access_hr_portal = True
        # For 'employee' role type, do NOT auto-set can_access_hr_portal
        # This allows admin to control access independently
        
        super().save(*args, **kwargs)


# =============================================================================
# NOTIFICATIONS
# =============================================================================

class Notification(models.Model):
    """In-app notifications for HR events"""
    NOTIFICATION_TYPE_CHOICES = [
        ('leave_request', 'Leave Request'),
        ('leave_approved', 'Leave Approved'),
        ('leave_rejected', 'Leave Rejected'),
        ('expense_request', 'Expense Request'),
        ('expense_approved', 'Expense Approved'),
        ('expense_rejected', 'Expense Rejected'),
        ('expense_paid', 'Expense Paid'),
        ('timesheet_reminder', 'Timesheet Reminder'),
        ('timesheet_approved', 'Timesheet Approved'),
        ('timesheet_rejected', 'Timesheet Rejected'),
        ('asset_assigned', 'Asset Assigned'),
        ('general', 'General'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hr_notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True, help_text="URL to related resource")
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"

    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()
