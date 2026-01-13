"""
URL configuration for booksstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponse
import os

def service_worker(request):
    """Serve service worker from root path for proper scope"""
    sw_path = os.path.join(settings.BASE_DIR, 'booksstore/static/sw.js')
    with open(sw_path, 'r') as f:
        return HttpResponse(f.read(), content_type='application/javascript')

def manifest(request):
    """Serve manifest from root path"""
    manifest_path = os.path.join(settings.BASE_DIR, 'booksstore/static/manifest.json')
    with open(manifest_path, 'r') as f:
        return HttpResponse(f.read(), content_type='application/manifest+json')

urlpatterns = [
    # PWA files at root
    path('sw.js', service_worker, name='service_worker'),
    path('manifest.json', manifest, name='manifest'),
    
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('books/', include('books.urls')),
    path('accounts/', include('accounts.urls')),
    path('library/', include('library.urls')),
    path('resume-builder/', include('resume_builder.urls')),
    path('roadmap/', include('roadmap.urls')),
    path('careers/', include('careers.urls')),
]

urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)