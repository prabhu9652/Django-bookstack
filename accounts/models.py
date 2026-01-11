from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserAccessStatus(models.Model):
    """Track user access status and approval workflow"""
    
    ACCESS_STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='access_status')
    status = models.CharField(max_length=20, choices=ACCESS_STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_users'
    )
    rejection_reason = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='', help_text='Admin notes about this user')
    
    class Meta:
        verbose_name = 'User Access Status'
        verbose_name_plural = 'User Access Statuses'
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"
    
    @property
    def is_approved(self):
        """Check if user has approved access"""
        return self.status == 'approved'
    
    @property
    def is_pending(self):
        """Check if user access is pending"""
        return self.status == 'pending'
    
    @property
    def is_rejected(self):
        """Check if user access is rejected"""
        return self.status == 'rejected'
    
    @property
    def is_suspended(self):
        """Check if user access is suspended"""
        return self.status == 'suspended'
    
    def approve(self, approved_by_user):
        """Approve user access"""
        self.status = 'approved'
        self.approved_at = timezone.now()
        self.approved_by = approved_by_user
        self.save()
        
        # Log the approval
        AccessLog.objects.create(
            user=self.user,
            action='approved',
            performed_by=approved_by_user,
            notes=f'Access approved by {approved_by_user.username}'
        )
    
    def reject(self, rejected_by_user, reason=''):
        """Reject user access"""
        self.status = 'rejected'
        self.rejection_reason = reason
        self.save()
        
        # Log the rejection
        AccessLog.objects.create(
            user=self.user,
            action='rejected',
            performed_by=rejected_by_user,
            notes=f'Access rejected by {rejected_by_user.username}. Reason: {reason}'
        )
    
    def suspend(self, suspended_by_user, reason=''):
        """Suspend user access"""
        self.status = 'suspended'
        self.rejection_reason = reason
        self.save()
        
        # Log the suspension
        AccessLog.objects.create(
            user=self.user,
            action='suspended',
            performed_by=suspended_by_user,
            notes=f'Access suspended by {suspended_by_user.username}. Reason: {reason}'
        )


class AccessRequest(models.Model):
    """Track access requests from users"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, default='', help_text='Optional message from user')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default='')
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='processed_requests'
    )
    
    class Meta:
        verbose_name = 'Access Request'
        verbose_name_plural = 'Access Requests'
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"Access request from {self.user.username} at {self.requested_at}"
    
    def mark_processed(self, processed_by_user):
        """Mark request as processed"""
        self.processed = True
        self.processed_at = timezone.now()
        self.processed_by = processed_by_user
        self.save()


class AccessLog(models.Model):
    """Audit log for all access-related actions"""
    
    ACTION_CHOICES = [
        ('requested', 'Access Requested'),
        ('approved', 'Access Approved'),
        ('rejected', 'Access Rejected'),
        ('suspended', 'Access Suspended'),
        ('content_accessed', 'Content Accessed'),
        ('pdf_downloaded', 'PDF Downloaded'),
        ('pdf_viewed', 'PDF Viewed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='performed_actions'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default='')
    resource_id = models.CharField(max_length=100, blank=True, default='', help_text='ID of accessed resource (e.g., book ID)')
    resource_type = models.CharField(max_length=50, blank=True, default='', help_text='Type of resource (e.g., book, pdf)')
    notes = models.TextField(blank=True, default='')
    
    class Meta:
        verbose_name = 'Access Log'
        verbose_name_plural = 'Access Logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} at {self.timestamp}"


# Signal to create UserAccessStatus when user is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_access_status(sender, instance, created, **kwargs):
    """Create UserAccessStatus when a new user is created"""
    if created and not instance.is_superuser:
        UserAccessStatus.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_access_status(sender, instance, **kwargs):
    """Save UserAccessStatus when user is saved"""
    if not instance.is_superuser and hasattr(instance, 'access_status'):
        instance.access_status.save()