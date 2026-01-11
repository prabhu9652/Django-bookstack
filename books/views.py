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

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        books = Book.objects.filter(name__icontains=search_term).order_by('name')
    else:
        books = Book.objects.all().order_by('name')

    paginator = Paginator(books, 8)  # Show 8 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(parent=None).order_by('name')

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

    template_data = {}
    template_data['title'] = 'Books'
    template_data['books'] = page_obj
    template_data['categories'] = categories
    template_data['search_term'] = search_term
    template_data['user_library_book_ids'] = user_library_book_ids
    template_data['access_context'] = access_context
    return render(request, 'books/index.html', {'template_data': template_data})


def category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    books = cat.books.all().order_by('name')

    paginator = Paginator(books, 8)  # Show 8 books per page
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

    template_data = {}
    template_data['title'] = f"Category: {cat.name}"
    template_data['books'] = page_obj
    template_data['category'] = cat
    template_data['categories'] = Category.objects.filter(parent=None).order_by('name')
    template_data['user_library_book_ids'] = user_library_book_ids
    template_data['access_context'] = access_context
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

        template_data = {}
        template_data['title'] = book.name
        template_data['book'] = book
        template_data['reviews'] = reviews
        template_data['category'] = category
        template_data['is_in_library'] = is_in_library
        template_data['access_context'] = access_context
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