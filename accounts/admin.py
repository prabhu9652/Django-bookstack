from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import UserAccessStatus, AccessRequest, AccessLog


class UserAccessStatusInline(admin.StackedInline):
    model = UserAccessStatus
    fk_name = 'user'  # Specify which ForeignKey to use
    can_delete = False
    verbose_name_plural = 'Access Status'
    fields = ('status', 'approved_by', 'approved_at', 'rejection_reason', 'notes')
    readonly_fields = ('requested_at', 'approved_at', 'approved_by')


class UserAdmin(BaseUserAdmin):
    inlines = (UserAccessStatusInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'access_status_display', 'date_joined')
    list_filter = BaseUserAdmin.list_filter + ('access_status__status',)
    
    def access_status_display(self, obj):
        try:
            status = obj.access_status
            color_map = {
                'pending': 'orange',
                'approved': 'green',
                'rejected': 'red',
                'suspended': 'purple'
            }
            color = color_map.get(status.status, 'gray')
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color,
                status.get_status_display()
            )
        except UserAccessStatus.DoesNotExist:
            return format_html('<span style="color: gray;">No Status</span>')
    
    access_status_display.short_description = 'Access Status'


@admin.register(UserAccessStatus)
class UserAccessStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'requested_at', 'approved_by', 'approved_at')
    list_filter = ('status', 'requested_at', 'approved_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('requested_at', 'approved_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'status')
        }),
        ('Timestamps', {
            'fields': ('requested_at', 'approved_at')
        }),
        ('Approval Information', {
            'fields': ('approved_by', 'rejection_reason')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'approved_by')
    
    actions = ['approve_selected', 'reject_selected', 'suspend_selected']
    
    def approve_selected(self, request, queryset):
        count = 0
        for access_status in queryset.filter(status__in=['pending', 'rejected']):
            access_status.approve(request.user)
            count += 1
        
        self.message_user(request, f'{count} users approved successfully.')
    approve_selected.short_description = "Approve selected users"
    
    def reject_selected(self, request, queryset):
        count = 0
        for access_status in queryset.filter(status__in=['pending', 'approved']):
            access_status.reject(request.user, 'Bulk rejection by admin')
            count += 1
        
        self.message_user(request, f'{count} users rejected successfully.')
    reject_selected.short_description = "Reject selected users"
    
    def suspend_selected(self, request, queryset):
        count = 0
        for access_status in queryset.filter(status='approved'):
            access_status.suspend(request.user, 'Bulk suspension by admin')
            count += 1
        
        self.message_user(request, f'{count} users suspended successfully.')
    suspend_selected.short_description = "Suspend selected users"


@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_at', 'processed', 'processed_by', 'processed_at', 'user_status')
    list_filter = ('processed', 'requested_at', 'processed_at')
    search_fields = ('user__username', 'user__email', 'message')
    readonly_fields = ('requested_at', 'processed_at', 'ip_address', 'user_agent')
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'message', 'requested_at')
        }),
        ('Processing Information', {
            'fields': ('processed', 'processed_by', 'processed_at')
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'processed_by', 'user__access_status')
    
    def user_status(self, obj):
        try:
            status = obj.user.access_status
            color_map = {
                'pending': 'orange',
                'approved': 'green',
                'rejected': 'red',
                'suspended': 'purple'
            }
            color = color_map.get(status.status, 'gray')
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color,
                status.get_status_display()
            )
        except UserAccessStatus.DoesNotExist:
            return format_html('<span style="color: gray;">No Status</span>')
    
    user_status.short_description = 'Current Status'
    
    actions = ['mark_processed', 'approve_users', 'reject_users']
    
    def mark_processed(self, request, queryset):
        count = queryset.filter(processed=False).update(
            processed=True,
            processed_by=request.user
        )
        self.message_user(request, f'{count} requests marked as processed.')
    mark_processed.short_description = "Mark selected requests as processed"
    
    def approve_users(self, request, queryset):
        count = 0
        for access_request in queryset.filter(processed=False):
            try:
                access_status = access_request.user.access_status
                if not access_status.is_approved:
                    access_status.approve(request.user)
                    access_request.mark_processed(request.user)
                    count += 1
            except UserAccessStatus.DoesNotExist:
                pass
        
        self.message_user(request, f'{count} users approved and requests processed.')
    approve_users.short_description = "Approve users and mark requests as processed"
    
    def reject_users(self, request, queryset):
        count = 0
        for access_request in queryset.filter(processed=False):
            try:
                access_status = access_request.user.access_status
                if access_status.is_pending:
                    access_status.reject(request.user, 'Request rejected by admin')
                    access_request.mark_processed(request.user)
                    count += 1
            except UserAccessStatus.DoesNotExist:
                pass
        
        self.message_user(request, f'{count} users rejected and requests processed.')
    reject_users.short_description = "Reject users and mark requests as processed"


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'performed_by', 'resource_type', 'resource_id', 'ip_address')
    list_filter = ('action', 'timestamp', 'resource_type')
    search_fields = ('user__username', 'user__email', 'notes', 'resource_id')
    readonly_fields = ('timestamp', 'ip_address', 'user_agent')
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Log Information', {
            'fields': ('user', 'action', 'timestamp', 'performed_by')
        }),
        ('Resource Information', {
            'fields': ('resource_type', 'resource_id')
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'performed_by')
    
    def has_add_permission(self, request):
        return False  # Logs should not be manually created
    
    def has_change_permission(self, request, obj=None):
        return False  # Logs should not be modified
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete logs


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Customize admin site headers
admin.site.site_header = "TechBookHub Administration"
admin.site.site_title = "TechBookHub Admin"
admin.site.index_title = "Welcome to TechBookHub Administration"