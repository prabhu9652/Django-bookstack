"""
Audit Service - Business logic for audit logging
"""

from django.utils import timezone
from ..models import AuditLog


class AuditService:
    """Service class for audit logging"""

    @staticmethod
    def log_action(action, entity_type, entity_id, performed_by, 
                   entity_description='', old_values=None, new_values=None,
                   comments='', request=None):
        """
        Create an audit log entry.
        
        Args:
            action: Action performed (create, update, delete, etc.)
            entity_type: Type of entity (employee, leave_request, etc.)
            entity_id: ID of the entity
            performed_by: User who performed the action
            entity_description: Human-readable description
            old_values: Previous values (for updates)
            new_values: New values (for creates/updates)
            comments: Additional comments
            request: HTTP request (for IP and user agent)
        
        Returns:
            AuditLog instance
        """
        ip_address = None
        user_agent = ''
        
        if request:
            ip_address = AuditService._get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        return AuditLog.objects.create(
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id),
            entity_description=entity_description,
            performed_by=performed_by,
            ip_address=ip_address,
            user_agent=user_agent,
            old_values=old_values or {},
            new_values=new_values or {},
            comments=comments
        )

    @staticmethod
    def _get_client_ip(request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def log_employee_action(action, employee, performed_by, old_values=None, 
                           new_values=None, comments='', request=None):
        """Log an employee-related action"""
        return AuditService.log_action(
            action=action,
            entity_type='employee',
            entity_id=employee.employee_id,
            performed_by=performed_by,
            entity_description=f"{employee.full_name} ({employee.employee_id})",
            old_values=old_values,
            new_values=new_values,
            comments=comments,
            request=request
        )

    @staticmethod
    def log_leave_action(action, leave_request, performed_by, comments='', request=None):
        """Log a leave request action"""
        return AuditService.log_action(
            action=action,
            entity_type='leave_request',
            entity_id=leave_request.request_id,
            performed_by=performed_by,
            entity_description=f"{leave_request.employee.full_name} - {leave_request.leave_type.name}",
            new_values={
                'status': leave_request.status,
                'start_date': str(leave_request.start_date),
                'end_date': str(leave_request.end_date),
                'total_days': str(leave_request.total_days),
            },
            comments=comments,
            request=request
        )

    @staticmethod
    def log_expense_action(action, expense_request, performed_by, comments='', request=None):
        """Log an expense request action"""
        return AuditService.log_action(
            action=action,
            entity_type='expense_request',
            entity_id=expense_request.request_id,
            performed_by=performed_by,
            entity_description=f"{expense_request.employee.full_name} - {expense_request.amount} {expense_request.currency}",
            new_values={
                'status': expense_request.status,
                'amount': str(expense_request.amount),
                'currency': expense_request.currency,
                'category': expense_request.category.name,
            },
            comments=comments,
            request=request
        )

    @staticmethod
    def log_timesheet_action(action, timesheet, performed_by, comments='', request=None):
        """Log a timesheet action"""
        return AuditService.log_action(
            action=action,
            entity_type='timesheet',
            entity_id=f"{timesheet.employee.employee_id}-{timesheet.week_start_date}",
            performed_by=performed_by,
            entity_description=f"{timesheet.employee.full_name} - Week of {timesheet.week_start_date}",
            new_values={
                'status': timesheet.status,
                'total_hours': str(timesheet.total_hours),
            },
            comments=comments,
            request=request
        )

    @staticmethod
    def log_asset_action(action, asset, performed_by, comments='', request=None):
        """Log an asset action"""
        return AuditService.log_action(
            action=action,
            entity_type='asset',
            entity_id=asset.asset_id,
            performed_by=performed_by,
            entity_description=f"{asset.name} ({asset.asset_id})",
            new_values={
                'status': asset.status,
                'condition': asset.condition,
                'assigned_to': asset.assigned_to.employee_id if asset.assigned_to else None,
            },
            comments=comments,
            request=request
        )

    @staticmethod
    def log_project_action(action, project, performed_by, comments='', request=None):
        """Log a project action"""
        return AuditService.log_action(
            action=action,
            entity_type='project',
            entity_id=project.project_id,
            performed_by=performed_by,
            entity_description=f"{project.name} ({project.project_id})",
            new_values={
                'status': project.status,
                'name': project.name,
            },
            comments=comments,
            request=request
        )

    @staticmethod
    def get_entity_history(entity_type, entity_id):
        """Get audit history for a specific entity"""
        return AuditLog.objects.filter(
            entity_type=entity_type,
            entity_id=str(entity_id)
        ).order_by('-performed_at')

    @staticmethod
    def get_user_activity(user, limit=50):
        """Get recent activity by a user"""
        return AuditLog.objects.filter(
            performed_by=user
        ).order_by('-performed_at')[:limit]

    @staticmethod
    def get_recent_activity(limit=100):
        """Get recent activity across the system"""
        return AuditLog.objects.select_related('performed_by').order_by('-performed_at')[:limit]

    @staticmethod
    def search_audit_logs(entity_type=None, action=None, user=None, 
                         start_date=None, end_date=None):
        """Search audit logs with filters"""
        queryset = AuditLog.objects.select_related('performed_by')
        
        if entity_type:
            queryset = queryset.filter(entity_type=entity_type)
        
        if action:
            queryset = queryset.filter(action=action)
        
        if user:
            queryset = queryset.filter(performed_by=user)
        
        if start_date:
            queryset = queryset.filter(performed_at__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(performed_at__lte=end_date)
        
        return queryset.order_by('-performed_at')
