from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home.index'),
    path('about/', views.about, name='home.about'),
    path('offline/', views.offline, name='home.offline'),
    path('app/', views.app, name='home.app'),
]