from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from books.models import Book, Category
from .models import UserLibrary
from accounts.access_control import (
    require_content_access, 
    user_has_content_access,
    get_user_access_context,
    log_access_attempt
)
import json
import logging

logger = logging.getLogger(__name__)

@require_content_access(redirect_url='accounts.access_denied')
def index(request):
    """User's personal library with category organization"""
    category_slug = request.GET.get('category')
    
    # Get user's library books
    library_books = UserLibrary.objects.filter(user=request.user).select_related('book', 'book__category')
    
    # Filter by category if specified
    if category_slug:
        if category_slug == 'uncategorized':
            library_books = library_books.filter(book__category__isnull=True)
        else:
            category = get_object_or_404(Category, slug=category_slug)
            library_books = library_books.filter(book__category=category)
    
    # Get categories that have books in user's library
    categories_with_books = Category.objects.filter(
        books__userlibrary__user=request.user
    ).distinct().order_by('name')
    
    # Count uncategorized books
    uncategorized_count = library_books.filter(book__category__isnull=True).count()
    
    # Get access context
    access_context = get_user_access_context(request.user)
    
    template_data = {
        'title': 'My Library',
        'library_books': library_books,
        'categories': categories_with_books,
        'uncategorized_count': uncategorized_count,
        'current_category': category_slug,
        'total_books': library_books.count(),
        'access_context': access_context
    }
    
    return render(request, 'library/index.html', {'template_data': template_data})

@require_content_access(ajax=True)
@require_POST
def add_book(request):
    """Add a book to user's library via AJAX"""
    try:
        # Log the request for debugging
        logger.info(f"Add book request from user {request.user.username}")
        
        data = json.loads(request.body)
        book_id = data.get('book_id')
        
        if not book_id:
            logger.warning("No book_id provided in request")
            return JsonResponse({'success': False, 'message': 'Book ID is required'})
        
        book = get_object_or_404(Book, id=book_id)
        logger.info(f"Adding book '{book.name}' to library for user {request.user.username}")
        
        # Check if book is already in library
        library_item, created = UserLibrary.objects.get_or_create(
            user=request.user, 
            book=book
        )
        
        if created:
            # Log the library addition
            log_access_attempt(
                user=request.user,
                action='content_accessed',
                request=request,
                resource_id=book_id,
                resource_type='library_add',
                notes=f'Added book "{book.name}" to library'
            )
            
            logger.info(f"Book '{book.name}' successfully added to library")
            return JsonResponse({
                'success': True, 
                'message': 'Added to library'
            })
        else:
            logger.info(f"Book '{book.name}' already in library")
            return JsonResponse({
                'success': False, 
                'message': 'Already in library'
            })
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return JsonResponse({'success': False, 'message': 'Invalid request data'})
    except Exception as e:
        logger.error(f"Unexpected error in add_book: {e}")
        return JsonResponse({'success': False, 'message': f'Server error: {str(e)}'})

@require_content_access(ajax=True)
@require_POST
def remove_book(request):
    """Remove a book from user's library via AJAX"""
    try:
        # Log the request for debugging
        logger.info(f"Remove book request from user {request.user.username}")
        
        data = json.loads(request.body)
        book_id = data.get('book_id')
        
        if not book_id:
            logger.warning("No book_id provided in request")
            return JsonResponse({'success': False, 'message': 'Book ID is required'})
        
        book = get_object_or_404(Book, id=book_id)
        logger.info(f"Removing book '{book.name}' from library for user {request.user.username}")
        
        # Remove book from library
        library_item = UserLibrary.objects.filter(user=request.user, book=book).first()
        if library_item:
            library_item.delete()
            
            # Log the library removal
            log_access_attempt(
                user=request.user,
                action='content_accessed',
                request=request,
                resource_id=book_id,
                resource_type='library_remove',
                notes=f'Removed book "{book.name}" from library'
            )
            
            logger.info(f"Book '{book.name}' successfully removed from library")
            return JsonResponse({
                'success': True, 
                'message': 'Removed from library'
            })
        else:
            logger.warning(f"Book '{book.name}' not found in user's library")
            return JsonResponse({'success': False, 'message': 'Book not found in library'})
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return JsonResponse({'success': False, 'message': 'Invalid request data'})
    except Exception as e:
        logger.error(f"Unexpected error in remove_book: {e}")
        return JsonResponse({'success': False, 'message': f'Server error: {str(e)}'})

@require_content_access(ajax=True)
@require_POST
def debug_ajax(request):
    """Debug endpoint to test AJAX functionality"""
    try:
        logger.info(f"Debug AJAX request from user {request.user.username}")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Content type: {request.content_type}")
        logger.info(f"Request body: {request.body}")
        
        data = json.loads(request.body)
        logger.info(f"Parsed data: {data}")
        
        return JsonResponse({
            'success': True,
            'message': 'Debug endpoint working',
            'user': request.user.username,
            'data_received': data
        })
        
    except Exception as e:
        logger.error(f"Debug AJAX error: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Debug error: {str(e)}'
        })