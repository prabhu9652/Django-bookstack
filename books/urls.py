from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='books.index'),
    path('category/<slug:slug>/', views.category, name='books.category'),
    path('<int:id>/view/', views.view_pdf, name='books.view'),
    path('<int:id>/download/', views.download_pdf, name='books.download'),
    path('<int:id>/', views.show, name='books.show'),
    path('<int:id>/review/create/', views.create_review, name='books.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='books.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='books.delete_review'),
]