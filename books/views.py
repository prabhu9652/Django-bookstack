from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Review, Category
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.core.paginator import Paginator
from django.db.models import Prefetch
from accounts.access_control import (
    require_content_access, 
    require_pdf_access, 
    user_has_content_access,
    get_user_access_context,
    log_access_attempt
)
import os
import logging

logger = logging.getLogger(__name__)


@require_pdf_access
def download_pdf(request, id):
    book = get_object_or_404(Book, id=id)
    # Ensure a PDF is available
    if not book.pdf:
        raise Http404("PDF not found")
    try:
        file_path = book.pdf.path
    except Exception:
        raise Http404("PDF file not found")

    if not os.path.exists(file_path):
        raise Http404("PDF file not found")

    fp = open(file_path, 'rb')
    response = FileResponse(fp, content_type='application/pdf')
    filename = os.path.basename(book.pdf.name)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@require_pdf_access
@xframe_options_sameorigin
def view_pdf(request, id):
    """Stream the PDF inline so authenticated users can view it in-browser (SAMEORIGIN allowed for embedding)."""
    book = get_object_or_404(Book, id=id)
    if not book.pdf:
        raise Http404("PDF not found")
    try:
        file_path = book.pdf.path
    except Exception:
        raise Http404("PDF file not found")

    if not os.path.exists(file_path):
        raise Http404("PDF file not found")

    fp = open(file_path, 'rb')
    response = FileResponse(fp, content_type='application/pdf')
    filename = os.path.basename(book.pdf.name)
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    # Ensure sameorigin framing allowed
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response


@require_pdf_access
def read_pdf(request, id):
    """PDF Reader page with embedded viewer and book info."""
    book = get_object_or_404(Book, id=id)
    if not book.pdf:
        raise Http404("PDF not found")
    
    # Check if book is in user's library
    is_in_library = False
    if request.user.is_authenticated:
        try:
            from library.models import UserLibrary
            is_in_library = UserLibrary.objects.filter(user=request.user, book=book).exists()
        except ImportError:
            pass
    
    # Get access context
    access_context = get_user_access_context(request.user)
    
    template_data = {
        'title': f'Reading: {book.name}',
        'book': book,
        'is_in_library': is_in_library,
        'access_context': access_context,
    }
    
    return render(request, 'books/read_pdf.html', {'template_data': template_data})

def index(request):
    from django.db.models import Q, Count
    
    # Get query parameters
    search_term = request.GET.get('search', '').strip()
    category_slug = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'name')
    
    # Base queryset with optimized loading
    books = Book.objects.select_related('category').all()
    
    # Store total count before filtering
    total_books = books.count()
    
    # Apply search filter (title, author)
    if search_term:
        books = books.filter(
            Q(name__icontains=search_term) |
            Q(author__icontains=search_term) |
            Q(category__name__icontains=search_term)
        )
    
    # Filter by category if specified
    if category_slug:
        books = books.filter(category__slug=category_slug)
    
    # Apply sorting
    if sort_by == 'name':
        books = books.order_by('name')
    elif sort_by == '-name':
        books = books.order_by('-name')
    elif sort_by == 'author':
        books = books.order_by('author', 'name')
    elif sort_by == '-created':
        books = books.order_by('-id')  # Using id as proxy for created date
    elif sort_by == 'created':
        books = books.order_by('id')
    else:
        books = books.order_by('name')
    
    # Count filtered results
    filtered_count = books.count()

    # Pagination
    paginator = Paginator(books, 12)  # Show 12 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get categories with book counts
    categories = Category.objects.filter(parent=None).annotate(
        book_count=Count('books')
    ).order_by('name')

    # Get user's library books if authenticated and has access
    user_library_book_ids = []
    if request.user.is_authenticated and user_has_content_access(request.user):
        try:
            from library.models import UserLibrary
            user_library_book_ids = list(
                UserLibrary.objects.filter(user=request.user).values_list('book_id', flat=True)
            )
        except ImportError:
            pass

    # Get access context for template
    access_context = get_user_access_context(request.user)

    template_data = {
        'title': 'Books',
        'books': page_obj,
        'categories': categories,
        'search_term': search_term,
        'current_category': category_slug,
        'sort_by': sort_by,
        'total_books': total_books,
        'filtered_count': filtered_count,
        'user_library_book_ids': user_library_book_ids,
        'access_context': access_context,
    }
    return render(request, 'books/index.html', {'template_data': template_data})


def category(request, slug):
    from django.db.models import Q, Count
    
    cat = get_object_or_404(Category, slug=slug)
    
    # Get query parameters
    search_term = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'name')
    
    # Base queryset
    books = cat.books.select_related('category').all()
    
    # Apply search filter
    if search_term:
        books = books.filter(
            Q(name__icontains=search_term) |
            Q(author__icontains=search_term)
        )
    
    # Apply sorting
    if sort_by == 'name':
        books = books.order_by('name')
    elif sort_by == '-name':
        books = books.order_by('-name')
    elif sort_by == 'author':
        books = books.order_by('author', 'name')
    elif sort_by == '-created':
        books = books.order_by('-id')
    elif sort_by == 'created':
        books = books.order_by('id')
    else:
        books = books.order_by('name')
    
    # Count filtered results
    filtered_count = books.count()

    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get user's library books if authenticated and has access
    user_library_book_ids = []
    if request.user.is_authenticated and user_has_content_access(request.user):
        try:
            from library.models import UserLibrary
            user_library_book_ids = list(
                UserLibrary.objects.filter(user=request.user).values_list('book_id', flat=True)
            )
        except ImportError:
            pass

    # Get access context for template
    access_context = get_user_access_context(request.user)
    
    # Get all categories with counts
    categories = Category.objects.filter(parent=None).annotate(
        book_count=Count('books')
    ).order_by('name')
    
    # Total books in this category
    total_books = cat.books.count()

    template_data = {
        'title': f"Category: {cat.name}",
        'books': page_obj,
        'category': cat,
        'categories': categories,
        'search_term': search_term,
        'current_category': slug,
        'sort_by': sort_by,
        'total_books': total_books,
        'filtered_count': filtered_count,
        'user_library_book_ids': user_library_book_ids,
        'access_context': access_context,
    }
    return render(request, 'books/index.html', {'template_data': template_data})

def show(request, id):
    try:
        # Use select_related to optimize database queries
        book = get_object_or_404(Book.objects.select_related('category'), id=id)
        reviews = Review.objects.filter(book=book).select_related('user')

        category_slug = request.GET.get('category')
        category = None
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
            except Category.DoesNotExist:
                pass

        # Check if book is in user's library (only for users with access)
        is_in_library = False
        if request.user.is_authenticated and user_has_content_access(request.user):
            try:
                from library.models import UserLibrary
                is_in_library = UserLibrary.objects.filter(user=request.user, book=book).exists()
            except ImportError:
                # Library app not available
                pass

        # Get access context for template
        access_context = get_user_access_context(request.user)

        # Debug logging for image issues
        logger.info(f"Book {id} cover field: {book.cover_image}")
        if book.cover_image:
            logger.info(f"Book {id} cover URL: {book.cover_image.url}")
        else:
            logger.info(f"Book {id} has no cover image")

        # Get PDF file size
        pdf_size = None
        pdf_size_display = None
        if book.pdf:
            try:
                pdf_size = book.pdf.size  # Size in bytes
                if pdf_size >= 1024 * 1024:  # >= 1 MB
                    pdf_size_display = f"{pdf_size / (1024 * 1024):.1f} MB"
                elif pdf_size >= 1024:  # >= 1 KB
                    pdf_size_display = f"{pdf_size / 1024:.0f} KB"
                else:
                    pdf_size_display = f"{pdf_size} bytes"
            except Exception as e:
                logger.warning(f"Could not get PDF size for book {id}: {e}")

        template_data = {}
        template_data['title'] = book.name
        template_data['book'] = book
        template_data['reviews'] = reviews
        template_data['category'] = category
        template_data['is_in_library'] = is_in_library
        template_data['access_context'] = access_context
        template_data['pdf_size'] = pdf_size
        template_data['pdf_size_display'] = pdf_size_display
        return render(request, 'books/show.html', {'template_data': template_data})
    except Exception as e:
        logger.error(f"Error loading book {id}: {str(e)}")
        raise Http404("Book not found")

@require_content_access
def create_review(request, id):
    try:
        book = get_object_or_404(Book, id=id)
        if request.method == 'POST' and request.POST['comment'] != '':
            review = Review()
            review.comment = request.POST['comment']
            review.book = book
            review.user = request.user
            review.save()
            return redirect('books.show', id=id)
        else:
            return redirect('books.show', id=id)
    except Exception as e:
        logger.error(f"Error creating review for book {id}: {str(e)}")
        return redirect('books.show', id=id)

@require_content_access
def edit_review(request, id, review_id):
    try:
        review = get_object_or_404(Review, id=review_id)
        if request.user != review.user:
            return redirect('books.show', id=id)

        if request.method == 'GET':
            template_data = {}
            template_data['title'] = 'Edit Review'
            template_data['review'] = review
            return render(request, 'books/edit_review.html', {'template_data': template_data})
        elif request.method == 'POST' and request.POST['comment'] != '':
            review.comment = request.POST['comment']
            review.save()
            return redirect('books.show', id=id)
        else:
            return redirect('books.show', id=id)
    except Exception as e:
        logger.error(f"Error editing review {review_id} for book {id}: {str(e)}")
        return redirect('books.show', id=id)

@require_content_access
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('books.show', id=id)