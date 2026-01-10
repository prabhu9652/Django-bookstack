from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='accounts.login'),
    path('logout/', views.custom_logout, name='accounts.logout'),
    path('signup/', views.signup, name='accounts.signup'),
    
    # Access Control URLs
    path('access-status/', views.access_status, name='accounts.access_status'),
    path('request-access/', views.request_access, name='accounts.request_access'),
    path('access-denied/', views.access_denied, name='accounts.access_denied'),
    
    # Admin URLs
    path('admin/access-requests/', views.admin_access_requests, name='accounts.admin_access_requests'),
    path('admin/approve-user/<int:user_id>/', views.approve_user_access, name='accounts.approve_user_access'),
    path('admin/reject-user/<int:user_id>/', views.reject_user_access, name='accounts.reject_user_access'),
    path('admin/suspend-user/<int:user_id>/', views.suspend_user_access, name='accounts.suspend_user_access'),
    
    # Password Reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]