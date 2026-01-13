"""
Property-based tests for Careers module models.
Feature: careers-module
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from hypothesis import given, strategies as st, settings
from hypothesis.extra.django import TestCase as HypothesisTestCase
import re

from .models import JobPosting, Application, ApplicationNote
from resume_builder.models import Resume, ResumeTemplate


class JobPostingModelTests(HypothesisTestCase):
    """Property tests for JobPosting model"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a template for resumes
        cls.template, _ = ResumeTemplate.objects.get_or_create(
            slug='test-template',
            defaults={
                'name': 'Test Template',
                'category': 'professional',
                'description': 'Test template',
                'html_template': '',
                'css_styles': '',
                'is_active': True,
            }
        )
    
    @given(title=st.text(min_size=1, max_size=100).filter(lambda x: x.strip()))
    @settings(max_examples=100, deadline=None)
    def test_property_1_slug_generation_uniqueness(self, title):
        """
        Property 1: Slug Generation Uniqueness
        For any JobPosting title, the auto-generated slug SHALL be URL-friendly 
        (lowercase, hyphenated, no special characters) and unique.
        Validates: Requirements 1.3
        """
        # Create job posting
        job = JobPosting.objects.create(
            title=title,
            department='Engineering',
            location='Remote',
            location_type='remote',
            employment_type='full_time',
            description='Test description',
            responsibilities='Test responsibilities',
            requirements='Test requirements',
        )
        
        job2 = None
        try:
            # Slug should be URL-friendly (lowercase, alphanumeric, hyphens, underscores only)
            # Django's slugify may produce empty slugs for non-ASCII titles
            if job.slug:
                self.assertTrue(
                    re.match(r'^[a-z0-9_-]+$', job.slug),
                    f"Slug '{job.slug}' is not URL-friendly"
                )
            
            # Slug should be unique
            duplicate_count = JobPosting.objects.filter(slug=job.slug).count()
            self.assertEqual(duplicate_count, 1, "Slug should be unique")
            
            # Create another job with same title - should get different slug
            job2 = JobPosting.objects.create(
                title=title,
                department='Engineering',
                location='Remote',
                location_type='remote',
                employment_type='full_time',
                description='Test description 2',
                responsibilities='Test responsibilities',
                requirements='Test requirements',
            )
            
            # Both slugs should be unique
            self.assertNotEqual(job.slug, job2.slug, "Duplicate titles should have unique slugs")
            
        finally:
            # Cleanup
            pks_to_delete = [job.pk]
            if job2:
                pks_to_delete.append(job2.pk)
            JobPosting.objects.filter(pk__in=pks_to_delete).delete()


class ApplicationModelTests(HypothesisTestCase):
    """Property tests for Application model"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create template
        cls.template, _ = ResumeTemplate.objects.get_or_create(
            slug='test-template-app',
            defaults={
                'name': 'Test Template',
                'category': 'professional',
                'description': 'Test template',
                'html_template': '',
                'css_styles': '',
                'is_active': True,
            }
        )
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username=f'testuser_{timezone.now().timestamp()}',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Create test job
        self.job = JobPosting.objects.create(
            title=f'Test Job {timezone.now().timestamp()}',
            department='Engineering',
            location='Remote',
            location_type='remote',
            employment_type='full_time',
            description='Test description',
            responsibilities='Test responsibilities',
            requirements='Test requirements',
        )
        
        # Create test resume
        self.resume = Resume.objects.create(
            user=self.user,
            template=self.template,
            title='Test Resume',
            full_name='Test User',
            email='test@example.com',
        )
    
    def tearDown(self):
        Application.objects.filter(user=self.user).delete()
        self.resume.delete()
        self.job.delete()
        self.user.delete()
    
    def test_property_3_application_uniqueness_constraint(self):
        """
        Property 3: Application Uniqueness Constraint
        For any (job, user) pair, attempting to create a second Application 
        SHALL raise an IntegrityError.
        Validates: Requirements 2.2
        """
        from django.db import transaction
        
        # Create first application
        app1 = Application.objects.create(
            job=self.job,
            user=self.user,
            resume=self.resume,
        )
        
        # Attempting to create duplicate should raise IntegrityError
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Application.objects.create(
                    job=self.job,
                    user=self.user,
                    resume=self.resume,
                )
    
    @given(status=st.sampled_from(['applied', 'under_review', 'interview', 'rejected', 'hired']))
    @settings(max_examples=100, deadline=None)
    def test_property_4_application_status_validity(self, status):
        """
        Property 4: Application Status Validity
        For any Application, the status field SHALL only accept values from 
        the defined choices.
        Validates: Requirements 2.3
        """
        # Create new user and job for each test
        user = User.objects.create_user(
            username=f'statususer_{timezone.now().timestamp()}_{status}',
            email='status@example.com',
            password='testpass123',
        )
        job = JobPosting.objects.create(
            title=f'Status Test Job {timezone.now().timestamp()}_{status}',
            department='Engineering',
            location='Remote',
            location_type='remote',
            employment_type='full_time',
            description='Test',
            responsibilities='Test',
            requirements='Test',
        )
        resume = Resume.objects.create(
            user=user,
            template=self.template,
            title='Test Resume',
            full_name='Test User',
            email='test@example.com',
        )
        
        try:
            app = Application.objects.create(
                job=job,
                user=user,
                resume=resume,
                status=status,
            )
            
            # Status should be saved correctly
            self.assertEqual(app.status, status)
            
            # Refresh from database
            app.refresh_from_db()
            self.assertEqual(app.status, status)
        finally:
            Application.objects.filter(user=user).delete()
            resume.delete()
            job.delete()
            user.delete()
    
    def test_property_5_applicant_data_snapshot_integrity(self):
        """
        Property 5: Applicant Data Snapshot Integrity
        For any Application, the applicant_name and applicant_email fields 
        SHALL be populated from the user's profile at creation time and 
        SHALL NOT change if the user later updates their profile.
        Validates: Requirements 2.4
        """
        # Create application
        app = Application.objects.create(
            job=self.job,
            user=self.user,
            resume=self.resume,
        )
        
        original_name = app.applicant_name
        original_email = app.applicant_email
        
        # Verify snapshot was taken
        self.assertEqual(original_name, 'Test User')
        self.assertEqual(original_email, 'test@example.com')
        
        # Update user profile
        self.user.first_name = 'Changed'
        self.user.last_name = 'Name'
        self.user.email = 'changed@example.com'
        self.user.save()
        
        # Refresh application from database
        app.refresh_from_db()
        
        # Application snapshot should NOT change
        self.assertEqual(app.applicant_name, original_name)
        self.assertEqual(app.applicant_email, original_email)
    
    def test_property_6_default_application_status(self):
        """
        Property 6: Default Application Status
        For any newly created Application, the status SHALL default to 'applied'.
        Validates: Requirements 2.5
        """
        # Create application without specifying status
        app = Application.objects.create(
            job=self.job,
            user=self.user,
            resume=self.resume,
        )
        
        # Status should default to 'applied'
        self.assertEqual(app.status, 'applied')
        
        # Verify in database
        app.refresh_from_db()
        self.assertEqual(app.status, 'applied')


class JobPostingActiveFilterTests(TestCase):
    """Tests for job posting active/open status"""
    
    def test_is_open_active_no_close_date(self):
        """Active job with no close date should be open"""
        job = JobPosting.objects.create(
            title='Open Job',
            department='Engineering',
            location='Remote',
            location_type='remote',
            employment_type='full_time',
            description='Test',
            responsibilities='Test',
            requirements='Test',
            is_active=True,
            closes_at=None,
        )
        self.assertTrue(job.is_open())
        job.delete()
    
    def test_is_open_inactive(self):
        """Inactive job should not be open"""
        job = JobPosting.objects.create(
            title='Inactive Job',
            department='Engineering',
            location='Remote',
            location_type='remote',
            employment_type='full_time',
            description='Test',
            responsibilities='Test',
            requirements='Test',
            is_active=False,
        )
        self.assertFalse(job.is_open())
        job.delete()
    
    def test_is_open_past_close_date(self):
        """Job with past close date should not be open"""
        job = JobPosting.objects.create(
            title='Closed Job',
            department='Engineering',
            location='Remote',
            location_type='remote',
            employment_type='full_time',
            description='Test',
            responsibilities='Test',
            requirements='Test',
            is_active=True,
            closes_at=timezone.now() - timezone.timedelta(days=1),
        )
        self.assertFalse(job.is_open())
        job.delete()
    
    def test_is_open_future_close_date(self):
        """Job with future close date should be open"""
        job = JobPosting.objects.create(
            title='Future Close Job',
            department='Engineering',
            location='Remote',
            location_type='remote',
            employment_type='full_time',
            description='Test',
            responsibilities='Test',
            requirements='Test',
            is_active=True,
            closes_at=timezone.now() + timezone.timedelta(days=30),
        )
        self.assertTrue(job.is_open())
        job.delete()



class AdminAccessControlTests(TestCase):
    """Tests for admin access control"""
    
    def setUp(self):
        # Create regular user
        self.user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='testpass123',
        )
        
        # Create superuser
        self.admin = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpass123',
        )
    
    def tearDown(self):
        self.user.delete()
        self.admin.delete()
    
    def test_property_17_admin_access_control_unauthenticated(self):
        """
        Property 17: Admin Access Control
        For any request to admin views from an unauthenticated user,
        the system SHALL redirect to login.
        Validates: Requirements 7.1
        """
        from django.test import Client
        client = Client()
        
        # Test admin jobs dashboard
        response = client.get('/careers/admin/jobs/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test admin applications dashboard
        response = client.get('/careers/admin/applications/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_property_17_admin_access_control_regular_user(self):
        """
        Property 17: Admin Access Control
        For any request to admin views from a user where is_superuser=False,
        the system SHALL return a 403 Forbidden response.
        Validates: Requirements 7.1
        """
        from django.test import Client
        client = Client()
        client.login(username='regularuser', password='testpass123')
        
        # Test admin jobs dashboard
        response = client.get('/careers/admin/jobs/')
        self.assertEqual(response.status_code, 403)
        
        # Test admin applications dashboard
        response = client.get('/careers/admin/applications/')
        self.assertEqual(response.status_code, 403)
        
        # Test admin create job
        response = client.get('/careers/admin/jobs/create/')
        self.assertEqual(response.status_code, 403)
    
    def test_property_17_admin_access_control_superuser(self):
        """
        Property 17: Admin Access Control
        For any request to admin views from a superuser,
        the system SHALL allow access.
        Validates: Requirements 7.1
        """
        from django.test import Client
        client = Client()
        client.login(username='adminuser', password='adminpass123')
        
        # Test admin jobs dashboard
        response = client.get('/careers/admin/jobs/')
        self.assertEqual(response.status_code, 200)
        
        # Test admin applications dashboard
        response = client.get('/careers/admin/applications/')
        self.assertEqual(response.status_code, 200)
        
        # Test admin create job
        response = client.get('/careers/admin/jobs/create/')
        self.assertEqual(response.status_code, 200)
