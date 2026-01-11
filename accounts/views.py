from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserAccessStatus, AccessRequest, AccessLog
from .access_control import (
    get_client_ip, 
    log_access_attempt, 
    user_has_content_access,
    admin_required,
    get_user_access_context
)


def signup(request):
    """User registration with automatic access status creation"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Log the registration
            log_access_attempt(
                user=user,
                action='requested',
                request=request,
                notes='User registered and access status created'
            )
            
            # Authenticate and login the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 
                    'Account created successfully! Your access is pending admin approval. '
                    'You can request access to view and download content.'
                )
                return redirect('accounts.access_status')
            else:
                messages.success(request, 
                    'Account created successfully! Please log in and request access to content.'
                )
                return redirect('accounts.login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def access_status(request):
    """Show user's current access status"""
    try:
        # Ensure user has access status
        try:
            access_status = request.user.access_status
        except UserAccessStatus.DoesNotExist:
            # Create access status if it doesn't exist
            access_status = UserAccessStatus.objects.create(user=request.user)
        
        # Get recent access requests
        recent_requests = AccessRequest.objects.filter(user=request.user)[:5]
        
        # Get access context
        access_context = get_user_access_context(request.user)
        
        context = {
            'access_status': access_status,
            'recent_requests': recent_requests,
            'access_context': access_context,
        }
        
        return render(request, 'accounts/access_status.html', context)
        
    except Exception as e:
        # Log the error
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in access_status for user {request.user.username}: {e}")
        
        messages.error(request, 'An error occurred while loading your access status. Please try again.')
        return redirect('home.index')


@login_required
@require_POST
@csrf_protect
def request_access(request):
    """Handle access request from user"""
    try:
        # Check if user already has access
        if user_has_content_access(request.user):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'You already have access to content.'
                })
            messages.info(request, 'You already have access to content.')
            return redirect('accounts.access_status')
        
        # Ensure user has access status
        try:
            access_status = request.user.access_status
        except UserAccessStatus.DoesNotExist:
            access_status = UserAccessStatus.objects.create(user=request.user)
        
        # Check if user already has a pending request
        existing_request = AccessRequest.objects.filter(
            user=request.user,
            processed=False
        ).first()
        
        if existing_request:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'You already have a pending access request.'
                })
            messages.warning(request, 'You already have a pending access request.')
            return redirect('accounts.access_status')
        
        # Create new access request
        message = request.POST.get('message', '').strip()
        access_request = AccessRequest.objects.create(
            user=request.user,
            message=message,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Log the request
        log_access_attempt(
            user=request.user,
            action='requested',
            request=request,
            notes=f'Access request submitted. Message: {message}'
        )
        
        messages.success(request, 
            '🎉 Access request submitted successfully! '
            'An administrator will review your request and notify you of the decision. '
            'Typical approval time is 24 hours or less.'
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Access request submitted successfully!'
            })
        
        return redirect('accounts.access_status')
        
    except Exception as e:
        # Log the error
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in request_access for user {request.user.username}: {e}")
        
        error_message = 'An error occurred while processing your request. Please try again.'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': error_message
            }, status=500)
        
        messages.error(request, error_message)
        return redirect('accounts.access_status')


@admin_required
def admin_access_requests(request):
    """Admin view to manage access requests"""
    # Get pending requests
    pending_requests = AccessRequest.objects.filter(processed=False).select_related('user')
    
    # Get users with different access statuses
    pending_users = UserAccessStatus.objects.filter(status='pending').select_related('user')
    approved_users = UserAccessStatus.objects.filter(status='approved').select_related('user', 'approved_by')
    rejected_users = UserAccessStatus.objects.filter(status='rejected').select_related('user')
    
    # Get recent access logs
    recent_logs = AccessLog.objects.all()[:20].select_related('user', 'performed_by')
    
    context = {
        'pending_requests': pending_requests,
        'pending_users': pending_users,
        'approved_users': approved_users,
        'rejected_users': rejected_users,
        'recent_logs': recent_logs,
    }
    
    return render(request, 'accounts/admin_access_requests.html', context)


@admin_required
@require_POST
@csrf_protect
def approve_user_access(request, user_id):
    """Approve user access"""
    user = get_object_or_404(User, id=user_id)
    
    try:
        access_status = user.access_status
    except UserAccessStatus.DoesNotExist:
        access_status = UserAccessStatus.objects.create(user=user)
    
    if access_status.is_approved:
        return JsonResponse({
            'success': False,
            'error': 'User already has approved access.'
        })
    
    # Approve the user
    access_status.approve(request.user)
    
    # Mark any pending requests as processed
    AccessRequest.objects.filter(user=user, processed=False).update(
        processed=True,
        processed_by=request.user
    )
    
    messages.success(request, f'Access approved for {user.username}.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Access approved for {user.username}.'
        })
    
    return redirect('accounts.admin_access_requests')


@admin_required
@require_POST
@csrf_protect
def reject_user_access(request, user_id):
    """Reject user access"""
    user = get_object_or_404(User, id=user_id)
    reason = request.POST.get('reason', '').strip()
    
    try:
        access_status = user.access_status
    except UserAccessStatus.DoesNotExist:
        access_status = UserAccessStatus.objects.create(user=user)
    
    # Reject the user
    access_status.reject(request.user, reason)
    
    # Mark any pending requests as processed
    AccessRequest.objects.filter(user=user, processed=False).update(
        processed=True,
        processed_by=request.user
    )
    
    messages.success(request, f'Access rejected for {user.username}.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Access rejected for {user.username}.'
        })
    
    return redirect('accounts.admin_access_requests')


@admin_required
@require_POST
@csrf_protect
def suspend_user_access(request, user_id):
    """Suspend user access"""
    user = get_object_or_404(User, id=user_id)
    reason = request.POST.get('reason', '').strip()
    
    try:
        access_status = user.access_status
    except UserAccessStatus.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User access status not found.'
        })
    
    if not access_status.is_approved:
        return JsonResponse({
            'success': False,
            'error': 'Cannot suspend user who is not approved.'
        })
    
    # Suspend the user
    access_status.suspend(request.user, reason)
    
    messages.success(request, f'Access suspended for {user.username}.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Access suspended for {user.username}.'
        })
    
    return redirect('accounts.admin_access_requests')


@login_required
def access_denied(request):
    """Access denied page"""
    access_context = get_user_access_context(request.user)
    return render(request, 'accounts/access_denied.html', {
        'access_context': access_context
    })


def custom_logout(request):
    """Custom logout view with proper error handling"""
    try:
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            messages.success(request, f'You have been successfully logged out.')
        else:
            messages.info(request, 'You were not logged in.')
    except Exception as e:
        # Log the error but still redirect
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error during logout: {e}")
        messages.warning(request, 'Logout completed with minor issues.')
    
    return redirect('home.index')