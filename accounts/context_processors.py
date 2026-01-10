"""
Context processors for accounts app
"""
from .access_control import get_user_access_context


def access_control_context(request):
    """
    Add access control context to all templates
    """
    try:
        if hasattr(request, 'user') and request.user and request.user.is_authenticated:
            return {
                'access_context': get_user_access_context(request.user)
            }
    except Exception as e:
        # Log the error but don't break the page
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in access_control_context: {e}")
    
    # Safe fallback for unauthenticated users or errors
    return {
        'access_context': {
            'has_content_access': False,
            'is_superuser': False,
            'access_status': None,
            'can_request_access': False,
            'access_status_display': 'Unknown'
        }
    }