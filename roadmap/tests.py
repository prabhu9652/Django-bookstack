from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import RoadmapPath, RoadmapPhase, RoadmapSkill


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RoadmapViewsTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test roadmap path
        self.roadmap_path = RoadmapPath.objects.create(
            name='Test Path',
            slug='test-path',
            subtitle='Test Subtitle',
            description='Test Description',
            icon_class='fas fa-test',
            difficulty='beginner',
            estimated_duration='1 month',
            order=1
        )
        
        # Create test phase
        self.phase = RoadmapPhase.objects.create(
            roadmap_path=self.roadmap_path,
            name='Test Phase',
            description='Test Phase Description',
            duration='2 weeks',
            order=1
        )
        
        # Create test skill
        self.skill = RoadmapSkill.objects.create(
            phase=self.phase,
            name='Test Skill',
            description='Test Skill Description',
            is_core=True,
            order=1
        )

    def test_roadmap_home_view(self):
        """Test roadmap home page loads correctly"""
        response = self.client.get(reverse('roadmap:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engineering Career Roadmaps')
        self.assertContains(response, 'Test Path')

    def test_roadmap_path_detail_view(self):
        """Test roadmap path detail page loads correctly"""
        response = self.client.get(reverse('roadmap:path_detail', kwargs={'slug': 'test-path'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Path')
        self.assertContains(response, 'Test Phase')
        self.assertContains(response, 'Test Skill')

    def test_api_path_detail_view(self):
        """Test API endpoint returns correct JSON data"""
        response = self.client.get(reverse('roadmap:api_path_detail', kwargs={'slug': 'test-path'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = response.json()
        self.assertEqual(data['name'], 'Test Path')
        self.assertEqual(len(data['phases']), 1)
        self.assertEqual(data['phases'][0]['name'], 'Test Phase')
        self.assertEqual(len(data['phases'][0]['skills']), 1)
        self.assertEqual(data['phases'][0]['skills'][0]['name'], 'Test Skill')

    def test_roadmap_path_not_found(self):
        """Test 404 for non-existent roadmap path"""
        response = self.client.get(reverse('roadmap:path_detail', kwargs={'slug': 'non-existent'}))
        self.assertEqual(response.status_code, 404)

    def test_api_path_not_found(self):
        """Test 404 for non-existent API path"""
        response = self.client.get(reverse('roadmap:api_path_detail', kwargs={'slug': 'non-existent'}))
        self.assertEqual(response.status_code, 404)