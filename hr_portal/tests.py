"""
HR Portal Tests - Access Control and Feature Toggle Tests

Tests for the admin-controlled HR Portal access system.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import HRRole, Employee, Department, Designation
from .permissions import (
    can_access_hr_portal, get_hr_role, is_employee,
    is_hr_admin, is_finance_admin, is_app_admin
)


class HRPortalAccessControlTests(TestCase):
    """Tests for HR Portal access control"""
    
    def setUp(self):
        """Set up test users and data"""
        self.client = Client()
        
        # Create test users
        self.user_no_role = User.objects.create_user(
            username='norole', password='testpass123', email='norole@test.com'
        )
        
        self.user_disabled = User.objects.create_user(
            username='disabled', password='testpass123', email='disabled@test.com'
        )
        HRRole.objects.create(
            user=self.user_disabled,
            can_access_hr_portal=False,
            is_employee=True,
            role_type='employee'
        )
        
        self.user_enabled = User.objects.create_user(
            username='enabled', password='testpass123', email='enabled@test.com'
        )
        HRRole.objects.create(
            user=self.user_enabled,
            can_access_hr_portal=True,
            is_employee=True,
            role_type='employee'
        )
        
        self.user_admin = User.objects.create_user(
            username='hradmin', password='testpass123', email='hradmin@test.com'
        )
        HRRole.objects.create(
            user=self.user_admin,
            can_access_hr_portal=True,
            is_employee=True,
            role_type='hr_admin'
        )
        
        self.superuser = User.objects.create_superuser(
            username='super', password='testpass123', email='super@test.com'
        )
    
    def test_user_without_role_cannot_access(self):
        """User without HR role should not have access"""
        self.assertFalse(can_access_hr_portal(self.user_no_role))
    
    def test_user_with_disabled_access_cannot_access(self):
        """User with can_access_hr_portal=False should not have access"""
        self.assertFalse(can_access_hr_portal(self.user_disabled))
    
    def test_user_with_enabled_access_can_access(self):
        """User with can_access_hr_portal=True should have access"""
        self.assertTrue(can_access_hr_portal(self.user_enabled))
    
    def test_superuser_always_has_access(self):
        """Superuser should always have access"""
        self.assertTrue(can_access_hr_portal(self.superuser))
    
    def test_access_toggle_takes_effect_immediately(self):
        """Changing can_access_hr_portal should take effect immediately"""
        # Initially enabled
        self.assertTrue(can_access_hr_portal(self.user_enabled))
        
        # Disable access
        hr_role = self.user_enabled.hr_role
        hr_role.can_access_hr_portal = False
        hr_role.save()
        
        # Clear the cached hr_role and refresh user
        if hasattr(self.user_enabled, '_hr_role_cache'):
            delattr(self.user_enabled, '_hr_role_cache')
        self.user_enabled.refresh_from_db()
        
        # Should now be denied
        self.assertFalse(can_access_hr_portal(self.user_enabled))
        
        # Re-enable access
        hr_role.refresh_from_db()
        hr_role.can_access_hr_portal = True
        hr_role.save()
        
        # Clear cache again
        if hasattr(self.user_enabled, '_hr_role_cache'):
            delattr(self.user_enabled, '_hr_role_cache')
        self.user_enabled.refresh_from_db()
        
        # Should now be allowed again
        self.assertTrue(can_access_hr_portal(self.user_enabled))


class HRPortalViewAccessTests(TestCase):
    """Tests for HR Portal view access control"""
    
    def setUp(self):
        """Set up test users"""
        self.client = Client()
        
        self.user_no_access = User.objects.create_user(
            username='noaccess', password='testpass123'
        )
        
        self.user_with_access = User.objects.create_user(
            username='withaccess', password='testpass123'
        )
        HRRole.objects.create(
            user=self.user_with_access,
            can_access_hr_portal=True,
            is_employee=True,
            role_type='employee'
        )
    
    def test_unauthenticated_user_redirected_to_login(self):
        """Unauthenticated user should be redirected to login"""
        response = self.client.get(reverse('hr_portal:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url.lower())
    
    def test_user_without_access_redirected_to_home(self):
        """User without HR access should be redirected to home"""
        self.client.login(username='noaccess', password='testpass123')
        response = self.client.get(reverse('hr_portal:dashboard'))
        self.assertEqual(response.status_code, 302)
        # Should redirect to home, not login
        self.assertNotIn('login', response.url.lower())
    
    def test_user_with_access_can_view_dashboard(self):
        """User with HR access should be able to view dashboard"""
        self.client.login(username='withaccess', password='testpass123')
        response = self.client.get(reverse('hr_portal:dashboard'))
        self.assertEqual(response.status_code, 200)


class HRRolePermissionTests(TestCase):
    """Tests for HR role-based permissions"""
    
    def setUp(self):
        """Set up test users with different roles"""
        self.employee = User.objects.create_user(username='emp', password='test')
        HRRole.objects.create(
            user=self.employee,
            can_access_hr_portal=True,
            is_employee=True,
            role_type='employee'
        )
        
        self.hr_admin = User.objects.create_user(username='hr', password='test')
        HRRole.objects.create(
            user=self.hr_admin,
            can_access_hr_portal=True,
            is_employee=True,
            role_type='hr_admin'
        )
        
        self.finance_admin = User.objects.create_user(username='fin', password='test')
        HRRole.objects.create(
            user=self.finance_admin,
            can_access_hr_portal=True,
            is_employee=True,
            role_type='finance_admin'
        )
        
        self.app_admin = User.objects.create_user(username='app', password='test')
        HRRole.objects.create(
            user=self.app_admin,
            can_access_hr_portal=True,
            is_employee=True,
            role_type='app_admin'
        )
    
    def test_employee_role_permissions(self):
        """Employee role should have basic access only"""
        self.assertTrue(is_employee(self.employee))
        self.assertFalse(is_hr_admin(self.employee))
        self.assertFalse(is_finance_admin(self.employee))
        self.assertFalse(is_app_admin(self.employee))
    
    def test_hr_admin_role_permissions(self):
        """HR Admin should have HR admin permissions"""
        self.assertTrue(is_employee(self.hr_admin))
        self.assertTrue(is_hr_admin(self.hr_admin))
        self.assertFalse(is_finance_admin(self.hr_admin))
        self.assertFalse(is_app_admin(self.hr_admin))
    
    def test_finance_admin_role_permissions(self):
        """Finance Admin should have finance permissions"""
        self.assertTrue(is_employee(self.finance_admin))
        self.assertFalse(is_hr_admin(self.finance_admin))
        self.assertTrue(is_finance_admin(self.finance_admin))
        self.assertFalse(is_app_admin(self.finance_admin))
    
    def test_app_admin_role_permissions(self):
        """App Admin should have all permissions"""
        self.assertTrue(is_employee(self.app_admin))
        self.assertTrue(is_hr_admin(self.app_admin))
        self.assertTrue(is_finance_admin(self.app_admin))
        self.assertTrue(is_app_admin(self.app_admin))


class HRRoleAutoPermissionsTests(TestCase):
    """Tests for automatic permission assignment based on role type"""
    
    def test_app_admin_gets_all_permissions(self):
        """App Admin role should auto-set all permissions"""
        user = User.objects.create_user(username='test', password='test')
        hr_role = HRRole.objects.create(
            user=user,
            role_type='app_admin'
        )
        
        self.assertTrue(hr_role.can_access_hr_portal)
        self.assertTrue(hr_role.is_employee)
        self.assertTrue(hr_role.can_manage_employees)
        self.assertTrue(hr_role.can_manage_leaves)
        self.assertTrue(hr_role.can_manage_expenses)
        self.assertTrue(hr_role.can_manage_assets)
        self.assertTrue(hr_role.can_manage_timesheets)
        self.assertTrue(hr_role.can_manage_projects)
        self.assertTrue(hr_role.can_manage_holidays)
        self.assertTrue(hr_role.can_view_reports)
    
    def test_hr_admin_gets_hr_permissions(self):
        """HR Admin role should auto-set HR-related permissions"""
        user = User.objects.create_user(username='test', password='test')
        hr_role = HRRole.objects.create(
            user=user,
            role_type='hr_admin'
        )
        
        self.assertTrue(hr_role.can_access_hr_portal)
        self.assertTrue(hr_role.can_manage_employees)
        self.assertTrue(hr_role.can_manage_leaves)
        self.assertTrue(hr_role.can_manage_assets)
        self.assertTrue(hr_role.can_manage_holidays)
        self.assertTrue(hr_role.can_view_reports)
        # Should NOT have finance permissions
        self.assertFalse(hr_role.can_manage_expenses)
    
    def test_finance_admin_gets_finance_permissions(self):
        """Finance Admin role should auto-set finance permissions"""
        user = User.objects.create_user(username='test', password='test')
        hr_role = HRRole.objects.create(
            user=user,
            role_type='finance_admin'
        )
        
        self.assertTrue(hr_role.can_access_hr_portal)
        self.assertTrue(hr_role.can_manage_expenses)
        self.assertTrue(hr_role.can_view_reports)
        # Should NOT have HR permissions
        self.assertFalse(hr_role.can_manage_employees)
        self.assertFalse(hr_role.can_manage_leaves)
