from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings


def superuser_required(view_func):
    """
    Decorator that checks if the user is a superuser.
    Returns 403 Forbidden if not a superuser.
    Redirects to login if not authenticated.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')
            return redirect(login_url)
        
        if not request.user.is_superuser:
            return HttpResponseForbidden(
                "You don't have permission to access this page."
            )
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
