"""
Asset Views - Asset management
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone

from ..permissions import (
    hr_portal_required, hr_admin_required,
    get_employee, is_hr_admin, can_manage_assets
)
from ..models import Asset, AssetCategory, AssetAssignment, Employee
from ..services import AssetService, AuditService


@hr_portal_required
def asset_dashboard(request):
    """Asset management dashboard"""
    employee = get_employee(request.user)
    
    context = {
        'title': 'Asset Management',
        'employee': employee,
    }
    
    if employee:
        # My assigned assets
        context['my_assets'] = Asset.objects.filter(
            assigned_to=employee
        ).select_related('category')
        
        # My asset history
        context['asset_history'] = AssetAssignment.objects.filter(
            employee=employee
        ).select_related('asset', 'asset__category').order_by('-assigned_date')[:10]
    
    # Admin view
    if can_manage_assets(request.user):
        context['all_assets'] = Asset.objects.select_related(
            'category', 'assigned_to'
        ).order_by('-created_at')[:20]
        context['asset_summary'] = AssetService.get_asset_summary()
        context['categories'] = AssetCategory.objects.filter(is_active=True)
    
    return render(request, 'hr_portal/asset/dashboard.html', context)


@hr_admin_required
def asset_list(request):
    """List all assets (admin view)"""
    category_id = request.GET.get('category')
    status = request.GET.get('status')
    
    assets = Asset.objects.select_related('category', 'assigned_to')
    
    if category_id:
        assets = assets.filter(category_id=category_id)
    if status:
        assets = assets.filter(status=status)
    
    context = {
        'title': 'All Assets',
        'assets': assets.order_by('asset_id'),
        'categories': AssetCategory.objects.filter(is_active=True),
        'status_choices': Asset.STATUS_CHOICES,
        'selected_category': category_id,
        'selected_status': status,
    }
    
    return render(request, 'hr_portal/asset/list.html', context)


@hr_admin_required
def asset_create(request):
    """Create a new asset"""
    if request.method == 'POST':
        try:
            category = get_object_or_404(AssetCategory, id=request.POST.get('category'))
            
            asset_data = {
                'asset_id': request.POST.get('asset_id'),
                'name': request.POST.get('name'),
                'category': category,
                'description': request.POST.get('description', ''),
                'serial_number': request.POST.get('serial_number', ''),
                'model': request.POST.get('model', ''),
                'manufacturer': request.POST.get('manufacturer', ''),
                'condition': request.POST.get('condition', 'new'),
                'location': request.POST.get('location', ''),
            }
            
            if request.POST.get('purchase_date'):
                from datetime import datetime
                asset_data['purchase_date'] = datetime.strptime(
                    request.POST.get('purchase_date'), '%Y-%m-%d'
                ).date()
            
            if request.POST.get('purchase_cost'):
                asset_data['purchase_cost'] = request.POST.get('purchase_cost')
            
            if request.POST.get('warranty_expiry'):
                from datetime import datetime
                asset_data['warranty_expiry'] = datetime.strptime(
                    request.POST.get('warranty_expiry'), '%Y-%m-%d'
                ).date()
            
            asset = AssetService.create_asset(asset_data, request.user)
            AuditService.log_asset_action('create', asset, request.user, request=request)
            messages.success(request, f'Asset {asset.asset_id} created successfully.')
            return redirect('hr_portal:asset_detail', asset_id=asset.asset_id)
        
        except Exception as e:
            messages.error(request, f'Error creating asset: {str(e)}')
    
    context = {
        'title': 'Add New Asset',
        'categories': AssetCategory.objects.filter(is_active=True),
        'condition_choices': Asset.CONDITION_CHOICES,
    }
    
    return render(request, 'hr_portal/asset/create.html', context)


@hr_portal_required
def asset_detail(request, asset_id):
    """View asset details"""
    asset = get_object_or_404(Asset, asset_id=asset_id)
    employee = get_employee(request.user)
    
    # Check permissions
    can_view = (
        asset.assigned_to == employee or
        can_manage_assets(request.user)
    )
    
    if not can_view:
        messages.error(request, 'You do not have permission to view this asset.')
        return redirect('hr_portal:asset_dashboard')
    
    # Get assignment history
    assignment_history = AssetAssignment.objects.filter(
        asset=asset
    ).select_related('employee', 'assigned_by').order_by('-assigned_date')
    
    context = {
        'title': f'Asset - {asset.asset_id}',
        'asset': asset,
        'assignment_history': assignment_history,
        'can_manage': can_manage_assets(request.user),
    }
    
    return render(request, 'hr_portal/asset/detail.html', context)


@hr_admin_required
@require_POST
def asset_assign(request, asset_id):
    """Assign asset to employee"""
    asset = get_object_or_404(Asset, asset_id=asset_id)
    employee = get_employee(request.user)
    
    if asset.status != 'available':
        messages.error(request, 'Asset is not available for assignment.')
        return redirect('hr_portal:asset_detail', asset_id=asset_id)
    
    try:
        assignee_id = request.POST.get('employee_id')
        assignee = get_object_or_404(Employee, id=assignee_id)
        notes = request.POST.get('notes', '')
        
        AssetService.assign_asset(asset, assignee, employee, notes)
        AuditService.log_asset_action('assign', asset, request.user, 
                                      comments=f'Assigned to {assignee.employee_id}', request=request)
        messages.success(request, f'Asset assigned to {assignee.full_name}.')
    except Exception as e:
        messages.error(request, f'Error assigning asset: {str(e)}')
    
    return redirect('hr_portal:asset_detail', asset_id=asset_id)


@hr_admin_required
@require_POST
def asset_return(request, asset_id):
    """Return asset from employee"""
    asset = get_object_or_404(Asset, asset_id=asset_id)
    employee = get_employee(request.user)
    
    if asset.status != 'assigned':
        messages.error(request, 'Asset is not currently assigned.')
        return redirect('hr_portal:asset_detail', asset_id=asset_id)
    
    try:
        condition = request.POST.get('condition', 'good')
        notes = request.POST.get('notes', '')
        
        previous_assignee = asset.assigned_to
        AssetService.return_asset(asset, employee, condition, notes)
        AuditService.log_asset_action('return', asset, request.user,
                                      comments=f'Returned from {previous_assignee.employee_id}', request=request)
        messages.success(request, 'Asset returned successfully.')
    except Exception as e:
        messages.error(request, f'Error returning asset: {str(e)}')
    
    return redirect('hr_portal:asset_detail', asset_id=asset_id)


@hr_admin_required
def asset_category_list(request):
    """List asset categories"""
    categories = AssetCategory.objects.all().order_by('name')
    
    context = {
        'title': 'Asset Categories',
        'categories': categories,
    }
    
    return render(request, 'hr_portal/asset/categories.html', context)


@hr_admin_required
@require_POST
def asset_category_create(request):
    """Create asset category"""
    try:
        AssetCategory.objects.create(
            name=request.POST.get('name'),
            code=request.POST.get('code'),
            description=request.POST.get('description', ''),
            depreciation_years=int(request.POST.get('depreciation_years', 3))
        )
        messages.success(request, 'Category created successfully.')
    except Exception as e:
        messages.error(request, f'Error creating category: {str(e)}')
    
    return redirect('hr_portal:asset_category_list')
