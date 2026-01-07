from django.shortcuts import render
from books.models import Book

def index(request):
    template_data = {}
    template_data['title'] = 'Books Store'
    template_data['books'] = Book.objects.all().order_by('-id')[:3]
    return render(request, 'home/index.html', {'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})