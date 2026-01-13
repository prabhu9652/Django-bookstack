"""
Holiday Views - Holiday calendar management
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime

from django.db import models

from ..permissions import (
    hr_portal_required, hr_admin_required,
    get_employee, can_manage_assets
)
from ..models import HolidayCalendar
from ..services import AuditService


@hr_portal_required
def holiday_calendar(request):
    """View holiday calendar"""
    year = int(request.GET.get('year', timezone.now().year))
    location = request.GET.get('location', '')
    
    holidays = HolidayCalendar.objects.filter(year=year, is_active=True)
    
    if location:
        holidays = holidays.filter(models.Q(location=location) | models.Q(location=''))
    
    # Get unique locations
    locations = HolidayCalendar.objects.exclude(
        location=''
    ).values_list('location', flat=True).distinct()
    
    context = {
        'title': f'Holiday Calendar {year}',
        'holidays': holidays.order_by('date'),
        'selected_year': year,
        'selected_location': location,
        'locations': locations,
        'years': range(timezone.now().year - 1, timezone.now().year + 3),
        'can_manage': can_manage_assets(request.user),
    }
    
    return render(request, 'hr_portal/holiday/calendar.html', context)
