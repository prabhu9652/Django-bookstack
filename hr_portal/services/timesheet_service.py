"""
Timesheet Service - Business logic for timesheet management
"""

from django.db import models, transaction
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from ..models import Timesheet, TimesheetEntry, Project, ProjectAssignment


class TimesheetService:
    """Service class for timesheet-related operations"""

    @staticmethod
    def get_week_dates(date=None):
        """Get Monday and Sunday of the week for a given date"""
        if date is None:
            date = timezone.now().date()
        
        # Get Monday (weekday 0)
        monday = date - timedelta(days=date.weekday())
        sunday = monday + timedelta(days=6)
        
        return monday, sunday

    @staticmethod
    def get_or_create_timesheet(employee, week_start_date=None):
        """Get or create a timesheet for the given week"""
        if week_start_date is None:
            week_start_date, _ = TimesheetService.get_week_dates()
        
        week_end_date = week_start_date + timedelta(days=6)
        
        timesheet, created = Timesheet.objects.get_or_create(
            employee=employee,
            week_start_date=week_start_date,
            defaults={'week_end_date': week_end_date}
        )
        
        return timesheet, created

    @staticmethod
    def get_employee_projects(employee):
        """Get projects assigned to an employee"""
        assignments = ProjectAssignment.objects.filter(
            employee=employee,
            is_active=True,
            project__is_active=True
        ).select_related('project')
        
        return [a.project for a in assignments]

    @staticmethod
    @transaction.atomic
    def add_timesheet_entry(timesheet, entry_data):
        """
        Add an entry to a timesheet.
        
        Args:
            timesheet: Timesheet instance
            entry_data: dict with entry fields
        
        Returns:
            TimesheetEntry instance
        """
        if timesheet.is_locked:
            raise ValueError("Timesheet is locked and cannot be modified")
        
        if timesheet.status == 'approved':
            raise ValueError("Approved timesheet cannot be modified")
        
        project = entry_data['project']
        date = entry_data['date']
        hours = entry_data['hours']
        
        # Validate date is within timesheet week
        if not (timesheet.week_start_date <= date <= timesheet.week_end_date):
            raise ValueError("Entry date must be within the timesheet week")
        
        # Validate hours
        if hours <= 0 or hours > 24:
            raise ValueError("Hours must be between 0 and 24")
        
        # Check total hours for the day
        existing_hours = TimesheetEntry.objects.filter(
            timesheet=timesheet,
            date=date
        ).exclude(project=project).aggregate(
            total=models.Sum('hours')
        )['total'] or Decimal('0')
        
        if existing_hours + hours > 24:
            raise ValueError(f"Total hours for {date} cannot exceed 24")
        
        # Create or update entry
        entry, created = TimesheetEntry.objects.update_or_create(
            timesheet=timesheet,
            project=project,
            date=date,
            defaults={
                'hours': hours,
                'description': entry_data.get('description', ''),
                'is_billable': entry_data.get('is_billable', True),
            }
        )
        
        return entry

    @staticmethod
    def get_timesheet_summary(timesheet):
        """Get summary of timesheet entries"""
        from django.db.models import Sum
        
        entries = timesheet.entries.all()
        
        # By project
        by_project = entries.values('project__name', 'project__project_id').annotate(
            total_hours=Sum('hours')
        )
        
        # By day
        by_day = entries.values('date').annotate(
            total_hours=Sum('hours')
        ).order_by('date')
        
        # Billable vs non-billable
        billable = entries.filter(is_billable=True).aggregate(total=Sum('hours'))['total'] or Decimal('0')
        non_billable = entries.filter(is_billable=False).aggregate(total=Sum('hours'))['total'] or Decimal('0')
        
        return {
            'total_hours': timesheet.total_hours,
            'by_project': list(by_project),
            'by_day': list(by_day),
            'billable_hours': billable,
            'non_billable_hours': non_billable,
        }

    @staticmethod
    def get_pending_approvals_for_manager(manager):
        """Get timesheets pending manager approval"""
        team_members = manager.direct_reports.filter(employment_status='active')
        return Timesheet.objects.filter(
            employee__in=team_members,
            status='submitted'
        ).select_related('employee')

    @staticmethod
    def get_employee_timesheet_history(employee, limit=10):
        """Get timesheet history for an employee"""
        return Timesheet.objects.filter(
            employee=employee
        ).order_by('-week_start_date')[:limit]

    @staticmethod
    @transaction.atomic
    def submit_timesheet(timesheet):
        """Submit timesheet for approval"""
        if timesheet.status != 'draft':
            raise ValueError("Only draft timesheets can be submitted")
        
        if timesheet.total_hours == 0:
            raise ValueError("Cannot submit timesheet with no entries")
        
        timesheet.submit()
        
        # Send notification to manager
        from .notification_service import NotificationService
        if timesheet.employee.reporting_manager:
            NotificationService.send_timesheet_notification(
                timesheet, 
                timesheet.employee.reporting_manager.user,
                'submitted'
            )
        
        return timesheet

    @staticmethod
    @transaction.atomic
    def approve_timesheet(timesheet, approved_by, comments=''):
        """Approve a timesheet"""
        if timesheet.status != 'submitted':
            raise ValueError("Timesheet is not pending approval")
        
        # Verify approver is the reporting manager
        if timesheet.employee.reporting_manager != approved_by:
            raise PermissionError("You are not authorized to approve this timesheet")
        
        timesheet.approve(approved_by, comments)
        
        # Send notification to employee
        from .notification_service import NotificationService
        NotificationService.send_timesheet_notification(timesheet, timesheet.employee.user, 'approved')
        
        return timesheet

    @staticmethod
    @transaction.atomic
    def reject_timesheet(timesheet, rejected_by, reason):
        """Reject a timesheet"""
        if timesheet.status != 'submitted':
            raise ValueError("Timesheet is not pending approval")
        
        timesheet.reject(rejected_by, reason)
        
        # Send notification to employee
        from .notification_service import NotificationService
        NotificationService.send_timesheet_notification(timesheet, timesheet.employee.user, 'rejected')
        
        return timesheet

    @staticmethod
    def get_project_hours_report(project, start_date=None, end_date=None):
        """Get hours logged on a project"""
        from django.db.models import Sum
        
        entries = TimesheetEntry.objects.filter(
            project=project,
            timesheet__status='approved'
        )
        
        if start_date:
            entries = entries.filter(date__gte=start_date)
        if end_date:
            entries = entries.filter(date__lte=end_date)
        
        # By employee
        by_employee = entries.values(
            'timesheet__employee__employee_id',
            'timesheet__employee__user__first_name',
            'timesheet__employee__user__last_name'
        ).annotate(total_hours=Sum('hours'))
        
        # By week
        by_week = entries.values('timesheet__week_start_date').annotate(
            total_hours=Sum('hours')
        ).order_by('timesheet__week_start_date')
        
        total = entries.aggregate(total=Sum('hours'))['total'] or Decimal('0')
        
        return {
            'total_hours': total,
            'by_employee': list(by_employee),
            'by_week': list(by_week),
        }
