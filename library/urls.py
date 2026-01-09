from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='library.index'),
    path('add/', views.add_book, name='library.add'),
    path('remove/', views.remove_book, name='library.remove'),
    path('debug/', views.debug_ajax, name='library.debug'),
]