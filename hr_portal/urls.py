"""
HR Portal URL Configuration
"""

from django.urls import path
from . import views

app_name = 'hr_portal'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Employee Management
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<str:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employees/<str:employee_id>/edit/', views.employee_edit, name='employee_edit'),
    path('profile/', views.my_profile, name='my_profile'),
    path('team/', views.my_team, name='my_team'),
    
    # Leave Management
    path('leave/', views.leave_dashboard, name='leave_dashboard'),
    path('leave/apply/', views.leave_request_create, name='leave_request_create'),
    path('leave/history/', views.leave_history, name='leave_history'),
    path('leave/calendar/', views.leave_calendar, name='leave_calendar'),
    path('leave/<str:request_id>/', views.leave_request_detail, name='leave_request_detail'),
    path('leave/<str:request_id>/submit/', views.leave_request_submit, name='leave_request_submit'),
    path('leave/<str:request_id>/approve/manager/', views.leave_approve_manager, name='leave_approve_manager'),
    path('leave/<str:request_id>/approve/hr/', views.leave_approve_hr, name='leave_approve_hr'),
    path('leave/<str:request_id>/reject/', views.leave_reject, name='leave_reject'),
    path('leave/<str:request_id>/cancel/', views.leave_request_cancel, name='leave_cancel'),
    
    # Expense Management
    path('expense/', views.expense_dashboard, name='expense_dashboard'),
    path('expense/submit/', views.expense_request_create, name='expense_request_create'),
    path('expense/history/', views.expense_history, name='expense_history'),
    path('expense/<str:request_id>/', views.expense_request_detail, name='expense_request_detail'),
    path('expense/<str:request_id>/submit/', views.expense_request_submit, name='expense_request_submit'),
    path('expense/<str:request_id>/approve/manager/', views.expense_approve_manager, name='expense_approve_manager'),
    path('expense/<str:request_id>/approve/finance/', views.expense_approve_finance, name='expense_approve_finance'),
    path('expense/<str:request_id>/paid/', views.expense_mark_paid, name='expense_mark_paid'),
    path('expense/<str:request_id>/reject/', views.expense_reject, name='expense_reject'),
    
    # Timesheet Management
    path('timesheet/', views.timesheet_dashboard, name='timesheet_dashboard'),
    path('timesheet/history/', views.timesheet_history, name='timesheet_history'),
    path('timesheet/<int:timesheet_id>/', views.timesheet_detail, name='timesheet_detail'),
    path('timesheet/<int:timesheet_id>/add-entry/', views.timesheet_add_entry, name='timesheet_add_entry'),
    path('timesheet/entry/<int:entry_id>/delete/', views.timesheet_delete_entry, name='timesheet_delete_entry'),
    path('timesheet/<int:timesheet_id>/submit/', views.timesheet_submit, name='timesheet_submit'),
    path('timesheet/<int:timesheet_id>/approve/', views.timesheet_approve, name='timesheet_approve'),
    path('timesheet/<int:timesheet_id>/reject/', views.timesheet_reject, name='timesheet_reject'),
]


urlpatterns += [
    # Asset Management
    path('assets/', views.asset_dashboard, name='asset_dashboard'),
    path('assets/list/', views.asset_list, name='asset_list'),
    path('assets/create/', views.asset_create, name='asset_create'),
    path('assets/categories/', views.asset_category_list, name='asset_category_list'),
    path('assets/categories/create/', views.asset_category_create, name='asset_category_create'),
    path('assets/<str:asset_id>/', views.asset_detail, name='asset_detail'),
    path('assets/<str:asset_id>/assign/', views.asset_assign, name='asset_assign'),
    path('assets/<str:asset_id>/return/', views.asset_return, name='asset_return'),
    
    # Project Management
    path('projects/', views.project_dashboard, name='project_dashboard'),
    path('projects/list/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<str:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<str:project_id>/add-member/', views.project_add_member, name='project_add_member'),
    path('projects/<str:project_id>/remove-member/<int:assignment_id>/', views.project_remove_member, name='project_remove_member'),
    path('projects/<str:project_id>/timesheet-report/', views.project_timesheet_report, name='project_timesheet_report'),
    
    # Holiday Calendar
    path('holidays/', views.holiday_calendar, name='holiday_calendar'),
    
    # Approvals
    path('approvals/', views.approval_dashboard, name='approval_dashboard'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Admin
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.user_management, name='user_management'),
    path('admin/users/<int:user_id>/assign-role/', views.assign_hr_role, name='assign_hr_role'),
    
    # API Endpoints
    path('api/employees/search/', views.api_employee_search, name='api_employee_search'),
    path('api/notifications/', views.api_notifications, name='api_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.api_mark_notification_read, name='api_mark_notification_read'),
    path('api/leave-balance/', views.api_leave_balance, name='api_leave_balance'),
    path('api/holidays/', views.api_holidays, name='api_holidays'),
    path('api/dashboard-stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
]
