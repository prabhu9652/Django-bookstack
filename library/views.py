from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from books.models import Book, Category
from .models import UserLibrary
import json

@login_required
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
    
    template_data = {
        'title': 'My Library',
        'library_books': library_books,
        'categories': categories_with_books,
        'uncategorized_count': uncategorized_count,
        'current_category': category_slug,
        'total_books': library_books.count()
    }
    
    return render(request, 'library/index.html', {'template_data': template_data})

@login_required
@require_POST
def add_book(request):
    """Add a book to user's library via AJAX"""
    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')
        
        if not book_id:
            return JsonResponse({'success': False, 'message': 'Book ID is required'})
        
        book = get_object_or_404(Book, id=book_id)
        
        # Check if book is already in library
        if UserLibrary.objects.filter(user=request.user, book=book).exists():
            return JsonResponse({'success': False, 'message': 'Book is already in your library'})
        
        # Add book to library
        UserLibrary.objects.create(user=request.user, book=book)
        
        return JsonResponse({
            'success': True, 
            'message': f'"{book.name}" has been added to your library'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred'})

@login_required
@require_POST
def remove_book(request):
    """Remove a book from user's library via AJAX"""
    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')
        
        if not book_id:
            return JsonResponse({'success': False, 'message': 'Book ID is required'})
        
        book = get_object_or_404(Book, id=book_id)
        
        # Remove book from library
        library_item = UserLibrary.objects.filter(user=request.user, book=book).first()
        if library_item:
            library_item.delete()
            return JsonResponse({
                'success': True, 
                'message': f'"{book.name}" has been removed from your library'
            })
        else:
            return JsonResponse({'success': False, 'message': 'Book not found in your library'})
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred'})