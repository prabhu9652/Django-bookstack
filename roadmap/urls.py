from django.urls import path
from . import views

app_name = 'roadmap'

urlpatterns = [
    path('', views.home, name='home'),
    path('path/<slug:slug>/', views.path_detail, name='path_detail'),
    path('api/path/<slug:slug>/', views.api_path_detail, name='api_path_detail'),
    path('api/skill/<int:skill_id>/progress/', views.update_progress, name='update_progress'),
    path('api/journey-skill/<int:skill_id>/progress/', views.update_journey_skill_progress, name='update_journey_skill_progress'),
]