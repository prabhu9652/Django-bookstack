from django.shortcuts import render
import logging
from books.models import Book, Category
from django.contrib.auth.models import User
from roadmap.models import RoadmapPath

logger = logging.getLogger(__name__)


def get_platform_stats():
    """
    Centralized function to get all platform statistics from the database.
    This ensures consistent counts across all views and prevents hard-coded values.
    
    Returns:
        dict: Dictionary containing all platform statistics
    """
    return {
        'total_books': Book.objects.count(),
        'total_categories': Category.objects.filter(parent=None).count(),  # Only top-level categories
        'total_users': User.objects.count(),
        'total_roadmaps': RoadmapPath.objects.filter(is_active=True).count(),
    }


def index(request):
    # Get dynamic platform statistics
    stats = get_platform_stats()
    
    template_data = {
        'title': 'Digital Library Platform',
        'recent_books': Book.objects.all().order_by('-id')[:8],
        # Dynamic counts from database - NO HARD-CODED VALUES
        'total_books': stats['total_books'],
        'total_categories': stats['total_categories'],
        'total_users': stats['total_users'],
        'total_roadmaps': stats['total_roadmaps'],
    }
    return render(request, 'home/index.html', {'template_data': template_data})

def about(request):
    # Get dynamic platform statistics for about page
    stats = get_platform_stats()
    
    template_data = {
        'title': 'About - Digital Library',
        # Dynamic counts from database - NO HARD-CODED VALUES
        'total_books': stats['total_books'],
        'total_categories': stats['total_categories'],
        'total_users': stats['total_users'],
        'total_roadmaps': stats['total_roadmaps'],
    }
    return render(request, 'home/about.html', {'template_data': template_data})


def offline(request):
    """Offline fallback page for PWA"""
    return render(request, 'offline.html')


def app(request):
    """PWA App download/install page"""
    template_data = {
        'title': 'Get the App - TechBookHub'
    }
    return render(request, 'home/app.html', {'template_data': template_data})