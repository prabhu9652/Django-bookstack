"""
Asset Service - Business logic for asset management
"""

from django.db import transaction
from django.utils import timezone
from ..models import Asset, AssetAssignment, AssetCategory


class AssetService:
    """Service class for asset-related operations"""

    @staticmethod
    @transaction.atomic
    def create_asset(asset_data, created_by=None):
        """
        Create a new asset.
        
        Args:
            asset_data: dict with asset fields
            created_by: User who is creating this asset
        
        Returns:
            Asset instance
        """
        # Generate asset ID
        category = asset_data['category']
        last_asset = Asset.objects.filter(category=category).order_by('-id').first()
        next_num = 1
        if last_asset:
            try:
                # Extract number from asset_id like "LAP0001"
                next_num = int(last_asset.asset_id[-4:]) + 1
            except (ValueError, IndexError):
                next_num = last_asset.id + 1
        
        asset_id = f"{category.code}{next_num:04d}"
        
        asset = Asset.objects.create(
            asset_id=asset_id,
            name=asset_data['name'],
            category=category,
            description=asset_data.get('description', ''),
            serial_number=asset_data.get('serial_number', ''),
            model=asset_data.get('model', ''),
            manufacturer=asset_data.get('manufacturer', ''),
            specifications=asset_data.get('specifications', {}),
            purchase_date=asset_data.get('purchase_date'),
            purchase_cost=asset_data.get('purchase_cost'),
            warranty_expiry=asset_data.get('warranty_expiry'),
            condition='new',
            status='available',
            location=asset_data.get('location', ''),
            created_by=created_by,
        )
        
        return asset

    @staticmethod
    @transaction.atomic
    def assign_asset(asset, employee, assigned_by=None, notes=''):
        """
        Assign an asset to an employee.
        
        Args:
            asset: Asset instance
            employee: Employee instance
            assigned_by: Employee who is assigning
            notes: Assignment notes
        
        Returns:
            AssetAssignment instance
        """
        if asset.status != 'available':
            raise ValueError(f"Asset is not available for assignment. Current status: {asset.status}")
        
        asset.assigned_to = employee
        asset.assigned_date = timezone.now().date()
        asset.status = 'assigned'
        asset.save()
        
        assignment = AssetAssignment.objects.create(
            asset=asset,
            employee=employee,
            assigned_by=assigned_by,
            assignment_type='assigned',
            notes=notes
        )
        
        # Send notification
        from .notification_service import NotificationService
        NotificationService.send_asset_notification(asset, employee.user, 'assigned')
        
        return assignment

    @staticmethod
    @transaction.atomic
    def return_asset(asset, returned_by=None, condition='good', notes=''):
        """
        Return an asset from an employee.
        
        Args:
            asset: Asset instance
            returned_by: Employee processing the return
            condition: Condition of returned asset
            notes: Return notes
        """
        if asset.status != 'assigned':
            raise ValueError("Asset is not currently assigned")
        
        if not asset.assigned_to:
            raise ValueError("Asset has no assigned employee")
        
        # Close current assignment
        current_assignment = AssetAssignment.objects.filter(
            asset=asset,
            employee=asset.assigned_to,
            returned_date__isnull=True
        ).first()
        
        if current_assignment:
            current_assignment.returned_date = timezone.now().date()
            current_assignment.return_condition = condition
            current_assignment.return_notes = notes
            current_assignment.save()
        
        asset.assigned_to = None
        asset.assigned_date = None
        asset.status = 'available'
        asset.condition = condition
        asset.save()

    @staticmethod
    @transaction.atomic
    def transfer_asset(asset, from_employee, to_employee, transferred_by=None, notes=''):
        """
        Transfer an asset from one employee to another.
        
        Args:
            asset: Asset instance
            from_employee: Current employee
            to_employee: New employee
            transferred_by: Employee processing the transfer
            notes: Transfer notes
        """
        if asset.assigned_to != from_employee:
            raise ValueError("Asset is not assigned to the specified employee")
        
        # Close current assignment
        current_assignment = AssetAssignment.objects.filter(
            asset=asset,
            employee=from_employee,
            returned_date__isnull=True
        ).first()
        
        if current_assignment:
            current_assignment.returned_date = timezone.now().date()
            current_assignment.return_notes = f"Transferred to {to_employee.employee_id}"
            current_assignment.save()
        
        # Create new assignment
        asset.assigned_to = to_employee
        asset.assigned_date = timezone.now().date()
        asset.save()
        
        AssetAssignment.objects.create(
            asset=asset,
            employee=to_employee,
            assigned_by=transferred_by,
            assignment_type='transferred',
            notes=notes
        )
        
        # Send notifications
        from .notification_service import NotificationService
        NotificationService.send_asset_notification(asset, to_employee.user, 'assigned')

    @staticmethod
    def get_available_assets(category=None):
        """Get available assets, optionally filtered by category"""
        queryset = Asset.objects.filter(status='available')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.select_related('category')

    @staticmethod
    def get_employee_assets(employee):
        """Get assets assigned to an employee"""
        return Asset.objects.filter(
            assigned_to=employee
        ).select_related('category')

    @staticmethod
    def get_asset_history(asset):
        """Get assignment history for an asset"""
        return AssetAssignment.objects.filter(
            asset=asset
        ).select_related('employee', 'assigned_by').order_by('-assigned_date')

    @staticmethod
    def get_asset_summary():
        """Get summary of all assets"""
        from django.db.models import Count
        
        total = Asset.objects.count()
        by_status = Asset.objects.values('status').annotate(count=Count('id'))
        by_category = Asset.objects.values('category__name').annotate(count=Count('id'))
        by_condition = Asset.objects.values('condition').annotate(count=Count('id'))
        
        return {
            'total': total,
            'by_status': {item['status']: item['count'] for item in by_status},
            'by_category': {item['category__name']: item['count'] for item in by_category},
            'by_condition': {item['condition']: item['count'] for item in by_condition},
        }

    @staticmethod
    def search_assets(query=None, category=None, status=None, condition=None):
        """Search assets with filters"""
        queryset = Asset.objects.select_related('category', 'assigned_to')
        
        if query:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(asset_id__icontains=query) |
                Q(name__icontains=query) |
                Q(serial_number__icontains=query) |
                Q(model__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(category=category)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if condition:
            queryset = queryset.filter(condition=condition)
        
        return queryset
