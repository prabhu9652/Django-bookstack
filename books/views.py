from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Review, Category
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.core.paginator import Paginator
from django.db.models import Prefetch
import os
import logging

logger = logging.getLogger(__name__)


@login_required
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


@login_required
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
        books = Book.objects.filter(name__icontains=search_term)
    else:
        books = Book.objects.all()

    paginator = Paginator(books, 8)  # Show 8 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(parent=None)

    template_data = {}
    template_data['title'] = 'Books'
    template_data['books'] = page_obj
    template_data['categories'] = categories
    template_data['search_term'] = search_term
    return render(request, 'books/index.html', {'template_data': template_data})


@login_required
def category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    books = cat.books.all()

    paginator = Paginator(books, 8)  # Show 8 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template_data = {}
    template_data['title'] = f"Category: {cat.name}"
    template_data['books'] = page_obj
    template_data['category'] = cat
    template_data['categories'] = Category.objects.filter(parent=None)
    return render(request, 'books/index.html', {'template_data': template_data})

def show(request, id):
    try:
        book = get_object_or_404(Book, id=id)
        reviews = Review.objects.filter(book=book)

        category_slug = request.GET.get('category')
        category = None
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
            except Category.DoesNotExist:
                pass

        template_data = {}
        template_data['title'] = book.name
        template_data['book'] = book
        template_data['reviews'] = reviews
        template_data['category'] = category
        return render(request, 'books/show.html', {'template_data': template_data})
    except Exception as e:
        logger.error(f"Error loading book {id}: {str(e)}")
        raise Http404("Book not found")

@login_required
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

@login_required
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

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('books.show', id=id)