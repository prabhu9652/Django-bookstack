"""
Custom middleware for the booksstore application.
"""
import os
from django.conf import settings


class MediaCacheMiddleware:
    """
    Middleware to add cache-control headers for media files (book covers, etc.)
    This improves performance by allowing browsers to cache images.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Cache duration: 7 days for media files
        self.cache_max_age = 60 * 60 * 24 * 7  # 7 days in seconds
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add cache headers for media files
        if request.path.startswith(settings.MEDIA_URL):
            # Check if it's an image file
            image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
            if any(request.path.lower().endswith(ext) for ext in image_extensions):
                response['Cache-Control'] = f'public, max-age={self.cache_max_age}, immutable'
                response['Vary'] = 'Accept-Encoding'
        
        return response
