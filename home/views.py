from django.shortcuts import render
import logging
from books.models import Book, Category
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def index(request):
    template_data = {}
    template_data['title'] = 'Digital Library Platform'
    template_data['recent_books'] = Book.objects.all().order_by('-id')[:8]
    template_data['total_books'] = Book.objects.count()
    template_data['total_categories'] = Category.objects.count()
    template_data['total_users'] = User.objects.count()
    return render(request, 'home/index.html', {'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About - Digital Library'
    return render(request, 'home/about.html', {'template_data': template_data})