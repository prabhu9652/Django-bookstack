"""
Access Control Utilities for Role-Based Access Control System
"""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.core.exceptions import PermissionDenied
from .models import UserAccessStatus, AccessLog


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_access_attempt(user, action, request, resource_id='', resource_type='', notes=''):
    """Log access attempts for audit purposes"""
    AccessLog.objects.create(
        user=user,
        action=action,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        resource_id=str(resource_id),
        resource_type=resource_type,
        notes=notes
    )


def user_has_content_access(user):
    """
    Check if user has access to protected content
    
    Rules:
    - Superusers always have access
    - Regular users must have approved access status
    """
    if not user or not user.is_authenticated:
        return False
    
    if user.is_superuser or user.is_staff:
        return True
    
    try:
        access_status = user.access_status
        return access_status.is_approved
    except UserAccessStatus.DoesNotExist:
        # Create access status if it doesn't exist
        try:
            UserAccessStatus.objects.create(user=user)
        except Exception:
            # If creation fails, just return False
            pass
        return False
    except Exception:
        # For any other errors, superusers get access, others don't
        return user.is_superuser or user.is_staff


def require_content_access(view_func=None, *, ajax=False, redirect_url=None):
    """
    Decorator to require approved content access
    
    Args:
        ajax: If True, return JSON response for AJAX requests
        redirect_url: Custom redirect URL for unauthorized access
    """
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if not user_has_content_access(request.user):
                # Log unauthorized access attempt
                log_access_attempt(
                    user=request.user,
                    action='content_accessed',
                    request=request,
                    notes='Unauthorized access attempt - access not approved'
                )
                
                if ajax or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'Access denied. Your account requires admin approval.',
                        'requires_approval': True
                    }, status=403)
                
                messages.error(request, 'Access denied. Your account requires admin approval to access content.')
                
                if redirect_url:
                    return redirect(redirect_url)
                
                # Render access denied page
                return render(request, 'accounts/access_denied.html', {
                    'user_status': getattr(request.user, 'access_status', None)
                }, status=403)
            
            # Log successful access
            log_access_attempt(
                user=request.user,
                action='content_accessed',
                request=request,
                notes='Authorized content access'
            )
            
            return func(request, *args, **kwargs)
        return wrapper
    
    if view_func is None:
        return decorator
    else:
        return decorator(view_func)


def require_pdf_access(view_func):
    """Decorator specifically for PDF access (download/view)"""
    @wraps(view_func)
    @require_content_access(ajax=False)
    def wrapper(request, *args, **kwargs):
        # Additional logging for PDF access
        book_id = kwargs.get('id') or args[0] if args else 'unknown'
        action = 'pdf_downloaded' if 'download' in view_func.__name__ else 'pdf_viewed'
        
        log_access_attempt(
            user=request.user,
            action=action,
            request=request,
            resource_id=book_id,
            resource_type='pdf',
            notes=f'PDF {action.split("_")[1]} for book {book_id}'
        )
        
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorator to require admin/superuser access"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            raise PermissionDenied("Admin access required")
        return view_func(request, *args, **kwargs)
    return wrapper


class AccessControlMixin:
    """Mixin for class-based views to enforce access control"""
    
    def dispatch(self, request, *args, **kwargs):
        if not user_has_content_access(request.user):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Access denied. Your account requires admin approval.',
                    'requires_approval': True
                }, status=403)
            
            messages.error(request, 'Access denied. Your account requires admin approval to access content.')
            return render(request, 'accounts/access_denied.html', {
                'user_status': getattr(request.user, 'access_status', None)
            }, status=403)
        
        return super().dispatch(request, *args, **kwargs)


def get_user_access_context(user):
    """Get access control context for templates"""
    if not user or not user.is_authenticated:
        return {
            'has_content_access': False,
            'is_superuser': False,
            'access_status': None,
            'can_request_access': False,
            'access_status_display': 'Not Authenticated'
        }
    
    try:
        has_access = user_has_content_access(user)
        
        # Safely get or create access status
        try:
            access_status = user.access_status
        except UserAccessStatus.DoesNotExist:
            # Create access status if it doesn't exist (for existing users)
            if not user.is_superuser:
                access_status = UserAccessStatus.objects.create(user=user)
            else:
                access_status = None
        
        return {
            'has_content_access': has_access,
            'is_superuser': user.is_superuser or user.is_staff,
            'access_status': access_status,
            'can_request_access': not has_access and not user.is_superuser and access_status and access_status.status in ['pending', 'rejected'],
            'access_status_display': access_status.get_status_display() if access_status else 'No Status'
        }
    except Exception as e:
        # Log error but return safe defaults
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in get_user_access_context for user {user.username}: {e}")
        
        return {
            'has_content_access': user.is_superuser or user.is_staff,
            'is_superuser': user.is_superuser or user.is_staff,
            'access_status': None,
            'can_request_access': False,
            'access_status_display': 'Error'
        }