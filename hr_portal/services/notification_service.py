"""
Notification Service - Business logic for notifications
"""

from django.utils import timezone
from ..models import Notification


class NotificationService:
    """Service class for notification-related operations"""

    @staticmethod
    def create_notification(recipient, notification_type, title, message, link=''):
        """
        Create a notification for a user.
        
        Args:
            recipient: User instance
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            link: Optional link to related resource
        
        Returns:
            Notification instance
        """
        return Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link
        )

    @staticmethod
    def send_leave_status_notification(leave_request, status):
        """Send notification for leave request status change"""
        status_messages = {
            'pending': ('Leave Request Submitted', f'Your leave request {leave_request.request_id} has been submitted for approval.'),
            'manager_approved': ('Leave Request - Manager Approved', f'Your leave request {leave_request.request_id} has been approved by your manager and is pending HR approval.'),
            'approved': ('Leave Request Approved', f'Your leave request {leave_request.request_id} has been approved. Enjoy your time off!'),
            'rejected': ('Leave Request Rejected', f'Your leave request {leave_request.request_id} has been rejected. Reason: {leave_request.rejection_reason}'),
        }
        
        if status in status_messages:
            title, message = status_messages[status]
            NotificationService.create_notification(
                recipient=leave_request.employee.user,
                notification_type=f'leave_{status}' if status != 'pending' else 'leave_request',
                title=title,
                message=message,
                link=f'/hr-portal/leaves/{leave_request.id}/'
            )
        
        # Notify manager for new requests
        if status == 'pending' and leave_request.employee.reporting_manager:
            NotificationService.create_notification(
                recipient=leave_request.employee.reporting_manager.user,
                notification_type='leave_request',
                title='New Leave Request',
                message=f'{leave_request.employee.full_name} has submitted a leave request for {leave_request.total_days} days.',
                link=f'/hr-portal/approvals/leaves/'
            )

    @staticmethod
    def send_expense_status_notification(expense_request, status):
        """Send notification for expense request status change"""
        status_messages = {
            'submitted': ('Expense Submitted', f'Your expense claim {expense_request.request_id} has been submitted for approval.'),
            'manager_approved': ('Expense - Manager Approved', f'Your expense claim {expense_request.request_id} has been approved by your manager and is pending finance approval.'),
            'finance_approved': ('Expense Approved', f'Your expense claim {expense_request.request_id} has been approved and is pending payment.'),
            'paid': ('Expense Paid', f'Your expense claim {expense_request.request_id} has been paid. Reference: {expense_request.payment_reference}'),
            'rejected': ('Expense Rejected', f'Your expense claim {expense_request.request_id} has been rejected. Reason: {expense_request.rejection_reason}'),
        }
        
        if status in status_messages:
            title, message = status_messages[status]
            NotificationService.create_notification(
                recipient=expense_request.employee.user,
                notification_type=f'expense_{status}' if status not in ['submitted'] else 'expense_request',
                title=title,
                message=message,
                link=f'/hr-portal/expenses/{expense_request.id}/'
            )
        
        # Notify manager for new requests
        if status == 'submitted' and expense_request.employee.reporting_manager:
            NotificationService.create_notification(
                recipient=expense_request.employee.reporting_manager.user,
                notification_type='expense_request',
                title='New Expense Claim',
                message=f'{expense_request.employee.full_name} has submitted an expense claim for {expense_request.amount} {expense_request.currency}.',
                link=f'/hr-portal/approvals/expenses/'
            )

    @staticmethod
    def send_timesheet_notification(timesheet, recipient, status):
        """Send notification for timesheet status change"""
        status_messages = {
            'submitted': ('Timesheet Submitted', f'Timesheet for week of {timesheet.week_start_date} has been submitted for approval.'),
            'approved': ('Timesheet Approved', f'Your timesheet for week of {timesheet.week_start_date} has been approved.'),
            'rejected': ('Timesheet Rejected', f'Your timesheet for week of {timesheet.week_start_date} has been rejected. Reason: {timesheet.rejection_reason}'),
        }
        
        if status in status_messages:
            title, message = status_messages[status]
            notification_type = 'timesheet_approved' if status == 'approved' else ('timesheet_rejected' if status == 'rejected' else 'timesheet_reminder')
            NotificationService.create_notification(
                recipient=recipient,
                notification_type=notification_type,
                title=title,
                message=message,
                link=f'/hr-portal/timesheets/{timesheet.id}/'
            )

    @staticmethod
    def send_asset_notification(asset, recipient, action):
        """Send notification for asset assignment"""
        if action == 'assigned':
            NotificationService.create_notification(
                recipient=recipient,
                notification_type='asset_assigned',
                title='Asset Assigned',
                message=f'Asset {asset.asset_id} ({asset.name}) has been assigned to you.',
                link=f'/hr-portal/assets/my-assets/'
            )

    @staticmethod
    def get_unread_notifications(user, limit=10):
        """Get unread notifications for a user"""
        return Notification.objects.filter(
            recipient=user,
            is_read=False
        ).order_by('-created_at')[:limit]

    @staticmethod
    def get_all_notifications(user, limit=50):
        """Get all notifications for a user"""
        return Notification.objects.filter(
            recipient=user
        ).order_by('-created_at')[:limit]

    @staticmethod
    def mark_as_read(notification_id, user):
        """Mark a notification as read"""
        try:
            notification = Notification.objects.get(id=notification_id, recipient=user)
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False

    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications as read for a user"""
        Notification.objects.filter(
            recipient=user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())

    @staticmethod
    def get_unread_count(user):
        """Get count of unread notifications"""
        return Notification.objects.filter(
            recipient=user,
            is_read=False
        ).count()
