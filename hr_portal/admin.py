"""
HR Portal Admin Configuration

Enterprise-grade admin interface for managing HR Portal access,
user roles, and feature toggles.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count

from .models import (
    HRRole, Employee, Department, Designation,
    LeaveType, LeaveRequest, LeaveBalance,
    ExpenseCategory, ExpenseRequest,
    AssetCategory, Asset, AssetAssignment,
    Project, ProjectAssignment,
    Timesheet, TimesheetEntry,
    HolidayCalendar, ApprovalWorkflow,
    AuditLog, Notification
)


# =============================================================================
# INLINE ADMIN FOR HR ROLE (attached to User)
# =============================================================================

class HRRoleInline(admin.StackedInline):
    """Inline admin for HR Role - appears on User admin page"""
    model = HRRole
    fk_name = 'user'  # Specify which FK to use (not created_by)
    can_delete = False
    verbose_name = 'HR Portal Access'
    verbose_name_plural = 'HR Portal Access'
    
    fieldsets = (
        ('Portal Access', {
            'fields': ('can_access_hr_portal', 'is_employee', 'role_type'),
            'description': 'Control whether this user can access the HR Portal'
        }),
        ('Permissions', {
            'fields': (
                ('can_manage_employees', 'can_manage_leaves'),
                ('can_manage_expenses', 'can_manage_assets'),
                ('can_manage_timesheets', 'can_manage_projects'),
                ('can_manage_holidays', 'can_view_reports'),
            ),
            'classes': ('collapse',),
            'description': 'Fine-grained permissions (auto-set based on role type)'
        }),
    )


# =============================================================================
# EXTENDED USER ADMIN
# =============================================================================

class UserAdminWithHRRole(BaseUserAdmin):
    """Extended User admin with HR Portal access controls"""
    inlines = [HRRoleInline]
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'hr_portal_access_badge', 'hr_role_badge', 'is_staff'
    )
    list_filter = BaseUserAdmin.list_filter + ('hr_role__can_access_hr_portal', 'hr_role__role_type')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    def hr_portal_access_badge(self, obj):
        """Display HR Portal access status as a colored badge"""
        try:
            if obj.hr_role.can_access_hr_portal:
                return format_html(
                    '<span style="background-color: #28a745; color: white; padding: 3px 10px; '
                    'border-radius: 3px; font-size: 11px;">✓ Enabled</span>'
                )
            else:
                return format_html(
                    '<span style="background-color: #dc3545; color: white; padding: 3px 10px; '
                    'border-radius: 3px; font-size: 11px;">✗ Disabled</span>'
                )
        except HRRole.DoesNotExist:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 10px; '
                'border-radius: 3px; font-size: 11px;">Not Set</span>'
            )
    hr_portal_access_badge.short_description = 'HR Portal'
    hr_portal_access_badge.admin_order_field = 'hr_role__can_access_hr_portal'
    
    def hr_role_badge(self, obj):
        """Display HR role type as a badge"""
        try:
            role = obj.hr_role
            colors = {
                'app_admin': '#6f42c1',
                'hr_admin': '#007bff',
                'finance_admin': '#17a2b8',
                'manager': '#fd7e14',
                'employee': '#28a745',
            }
            color = colors.get(role.role_type, '#6c757d')
            return format_html(
                '<span style="background-color: {}; color: white; padding: 3px 10px; '
                'border-radius: 3px; font-size: 11px;">{}</span>',
                color, role.get_role_type_display()
            )
        except HRRole.DoesNotExist:
            return '-'
    hr_role_badge.short_description = 'Role'
    hr_role_badge.admin_order_field = 'hr_role__role_type'

    def get_inline_instances(self, request, obj=None):
        """Only show HR Role inline when editing existing users"""
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


# Unregister default User admin and register our extended version
admin.site.unregister(User)
admin.site.register(User, UserAdminWithHRRole)


# =============================================================================
# HR ROLE ADMIN (Standalone)
# =============================================================================

@admin.register(HRRole)
class HRRoleAdmin(admin.ModelAdmin):
    """Standalone HR Role admin for bulk management"""
    list_display = (
        'user', 'access_badge', 'role_badge', 'is_employee',
        'permissions_summary', 'updated_at'
    )
    list_filter = ('can_access_hr_portal', 'role_type', 'is_employee')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_editable = ('is_employee',)
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    ordering = ('-updated_at',)
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Portal Access Control', {
            'fields': ('can_access_hr_portal', 'is_employee', 'role_type'),
            'description': 'Toggle HR Portal access for this user. Changes take effect immediately.'
        }),
        ('Granular Permissions', {
            'fields': (
                ('can_manage_employees', 'can_manage_leaves'),
                ('can_manage_expenses', 'can_manage_assets'),
                ('can_manage_timesheets', 'can_manage_projects'),
                ('can_manage_holidays', 'can_view_reports'),
            ),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['enable_hr_portal', 'disable_hr_portal', 'set_role_employee', 'set_role_manager']
    
    def access_badge(self, obj):
        if obj.can_access_hr_portal:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; '
                'border-radius: 3px; font-size: 11px;">✓ Enabled</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">✗ Disabled</span>'
        )
    access_badge.short_description = 'Portal Access'
    access_badge.admin_order_field = 'can_access_hr_portal'
    
    def role_badge(self, obj):
        colors = {
            'app_admin': '#6f42c1',
            'hr_admin': '#007bff',
            'finance_admin': '#17a2b8',
            'manager': '#fd7e14',
            'employee': '#28a745',
        }
        color = colors.get(obj.role_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_role_type_display()
        )
    role_badge.short_description = 'Role'
    role_badge.admin_order_field = 'role_type'
    
    def permissions_summary(self, obj):
        perms = []
        if obj.can_manage_employees: perms.append('Emp')
        if obj.can_manage_leaves: perms.append('Leave')
        if obj.can_manage_expenses: perms.append('Exp')
        if obj.can_manage_assets: perms.append('Asset')
        if obj.can_manage_timesheets: perms.append('TS')
        if obj.can_manage_projects: perms.append('Proj')
        if obj.can_view_reports: perms.append('Rpt')
        return ', '.join(perms) if perms else '-'
    permissions_summary.short_description = 'Permissions'
    
    @admin.action(description='Enable HR Portal access for selected users')
    def enable_hr_portal(self, request, queryset):
        updated = queryset.update(can_access_hr_portal=True)
        self.message_user(request, f'HR Portal access enabled for {updated} user(s).')
    
    @admin.action(description='Disable HR Portal access for selected users')
    def disable_hr_portal(self, request, queryset):
        updated = queryset.update(can_access_hr_portal=False)
        self.message_user(request, f'HR Portal access disabled for {updated} user(s).')
    
    @admin.action(description='Set role to Employee')
    def set_role_employee(self, request, queryset):
        for hr_role in queryset:
            hr_role.role_type = 'employee'
            hr_role.save()
        self.message_user(request, f'Role set to Employee for {queryset.count()} user(s).')
    
    @admin.action(description='Set role to Manager')
    def set_role_manager(self, request, queryset):
        for hr_role in queryset:
            hr_role.role_type = 'manager'
            hr_role.save()
        self.message_user(request, f'Role set to Manager for {queryset.count()} user(s).')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# =============================================================================
# EMPLOYEE ADMIN
# =============================================================================

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_id', 'full_name', 'department', 'designation',
        'employment_status', 'reporting_manager', 'joining_date'
    )
    list_filter = ('department', 'employment_status', 'employment_type')
    search_fields = ('employee_id', 'user__username', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user', 'reporting_manager')
    readonly_fields = ('created_at', 'updated_at')
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Name'


# =============================================================================
# ORGANIZATION STRUCTURE
# =============================================================================

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'head', 'is_active', 'employee_count')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    
    def employee_count(self, obj):
        return obj.employees.filter(employment_status='active').count()
    employee_count.short_description = 'Employees'


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'level', 'is_active')
    list_filter = ('department', 'is_active', 'level')
    search_fields = ('title',)


# =============================================================================
# LEAVE MANAGEMENT
# =============================================================================

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'default_days', 'is_paid', 'requires_approval', 'is_active')
    list_filter = ('is_paid', 'is_carry_forward', 'requires_approval', 'is_active')
    search_fields = ('name', 'code')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        'request_id', 'employee', 'leave_type', 'start_date', 
        'end_date', 'total_days', 'status'
    )
    list_filter = ('status', 'leave_type', 'created_at')
    search_fields = ('request_id', 'employee__employee_id', 'employee__user__username')
    readonly_fields = ('request_id', 'created_at', 'updated_at')
    date_hierarchy = 'start_date'


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'year', 'allocated_days', 'used_days', 'available_days')
    list_filter = ('year', 'leave_type')
    search_fields = ('employee__employee_id',)


# =============================================================================
# EXPENSE MANAGEMENT
# =============================================================================

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'max_amount', 'requires_receipt', 'is_active')
    list_filter = ('requires_receipt', 'is_active')


@admin.register(ExpenseRequest)
class ExpenseRequestAdmin(admin.ModelAdmin):
    list_display = (
        'request_id', 'employee', 'category', 'amount', 
        'currency', 'expense_date', 'status'
    )
    list_filter = ('status', 'category', 'currency')
    search_fields = ('request_id', 'employee__employee_id', 'title')
    readonly_fields = ('request_id', 'created_at', 'updated_at')
    date_hierarchy = 'expense_date'


# =============================================================================
# ASSET MANAGEMENT
# =============================================================================

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'depreciation_years', 'is_active')
    list_filter = ('is_active',)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'asset_id', 'name', 'category', 'status', 
        'condition', 'assigned_to', 'location'
    )
    list_filter = ('status', 'condition', 'category')
    search_fields = ('asset_id', 'name', 'serial_number')
    raw_id_fields = ('assigned_to',)


@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ('asset', 'employee', 'assigned_date', 'returned_date', 'assignment_type')
    list_filter = ('assignment_type', 'assigned_date')
    search_fields = ('asset__asset_id', 'employee__employee_id')


# =============================================================================
# PROJECT MANAGEMENT
# =============================================================================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'project_id', 'name', 'status', 'project_manager',
        'start_date', 'is_billable', 'is_active'
    )
    list_filter = ('status', 'is_billable', 'is_active', 'department')
    search_fields = ('project_id', 'name', 'client')
    raw_id_fields = ('project_manager',)


@admin.register(ProjectAssignment)
class ProjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ('project', 'employee', 'role', 'allocation_percentage', 'is_active')
    list_filter = ('role', 'is_active')


# =============================================================================
# TIMESHEET MANAGEMENT
# =============================================================================

class TimesheetEntryInline(admin.TabularInline):
    model = TimesheetEntry
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = (
        'employee', 'week_start_date', 'week_end_date',
        'total_hours', 'status', 'is_locked'
    )
    list_filter = ('status', 'is_locked')
    search_fields = ('employee__employee_id',)
    inlines = [TimesheetEntryInline]
    date_hierarchy = 'week_start_date'


# =============================================================================
# HOLIDAY & WORKFLOW
# =============================================================================

@admin.register(HolidayCalendar)
class HolidayCalendarAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'holiday_type', 'location', 'year', 'is_active')
    list_filter = ('holiday_type', 'year', 'is_active', 'location')
    search_fields = ('name',)
    date_hierarchy = 'date'


@admin.register(ApprovalWorkflow)
class ApprovalWorkflowAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'request_type', 'requires_manager_approval',
        'requires_hr_approval', 'requires_finance_approval', 'is_active'
    )
    list_filter = ('request_type', 'is_active')


# =============================================================================
# AUDIT & NOTIFICATIONS
# =============================================================================

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'performed_at', 'action', 'entity_type', 'entity_id',
        'performed_by', 'ip_address'
    )
    list_filter = ('action', 'entity_type', 'performed_at')
    search_fields = ('entity_id', 'entity_description', 'performed_by__username')
    readonly_fields = (
        'action', 'entity_type', 'entity_id', 'entity_description',
        'performed_by', 'performed_at', 'ip_address', 'user_agent',
        'old_values', 'new_values', 'comments'
    )
    date_hierarchy = 'performed_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'title', 'message')
    readonly_fields = ('created_at', 'read_at')


# =============================================================================
# ADMIN SITE CUSTOMIZATION
# =============================================================================

admin.site.site_header = 'HR Portal Administration'
admin.site.site_title = 'HR Portal Admin'
admin.site.index_title = 'HR Portal Management'
