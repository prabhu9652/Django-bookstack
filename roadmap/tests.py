from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import RoadmapPath, RoadmapPhase, RoadmapSkill, JourneySkill
from hypothesis import given, settings, strategies as st
from hypothesis.extra.django import TestCase as HypothesisTestCase


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
        self.assertContains(response, 'Navigate Your Engineering Journey')
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



# ============================================
# JOURNEY SKILL TESTS
# Feature: roadmap-skills-enhancement
# ============================================

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class JourneySkillModelTestCase(TestCase):
    """Unit tests for JourneySkill model"""
    
    def setUp(self):
        """Set up test data"""
        self.roadmap_path = RoadmapPath.objects.create(
            name='Test DevOps Path',
            slug='test-devops',
            subtitle='Test Subtitle',
            description='Test Description',
            icon_class='fas fa-server',
            difficulty='intermediate',
            estimated_duration='6 months',
            order=1
        )
    
    def test_journey_skill_creation(self):
        """Test JourneySkill can be created with all required fields"""
        skill = JourneySkill.objects.create(
            roadmap_path=self.roadmap_path,
            name='Docker',
            icon_class='fab fa-docker',
            display_order=1,
            is_active=True
        )
        self.assertEqual(skill.name, 'Docker')
        self.assertEqual(skill.icon_class, 'fab fa-docker')
        self.assertEqual(skill.display_order, 1)
        self.assertTrue(skill.is_active)
    
    def test_journey_skill_str_representation(self):
        """Test JourneySkill string representation"""
        skill = JourneySkill.objects.create(
            roadmap_path=self.roadmap_path,
            name='Kubernetes',
            icon_class='fas fa-dharmachakra',
            display_order=2
        )
        self.assertEqual(str(skill), 'Test DevOps Path - Kubernetes')
    
    def test_journey_skill_default_values(self):
        """Test JourneySkill default values"""
        skill = JourneySkill.objects.create(
            roadmap_path=self.roadmap_path,
            name='Test Skill'
        )
        self.assertEqual(skill.icon_class, 'fas fa-code')
        self.assertEqual(skill.display_order, 0)
        self.assertTrue(skill.is_active)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class JourneySkillViewTestCase(TestCase):
    """Unit tests for JourneySkill in views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.roadmap_path = RoadmapPath.objects.create(
            name='Test Full Stack Path',
            slug='test-fullstack',
            subtitle='Test Subtitle',
            description='Test Description',
            icon_class='fas fa-code',
            difficulty='intermediate',
            estimated_duration='12 months',
            order=1
        )
        
        # Create test phase for the path
        self.phase = RoadmapPhase.objects.create(
            roadmap_path=self.roadmap_path,
            name='Foundation',
            description='Foundation phase',
            duration='3 months',
            order=1
        )
        
        # Create journey skills
        self.skill1 = JourneySkill.objects.create(
            roadmap_path=self.roadmap_path,
            name='Python',
            icon_class='fab fa-python',
            display_order=1,
            is_active=True
        )
        self.skill2 = JourneySkill.objects.create(
            roadmap_path=self.roadmap_path,
            name='JavaScript',
            icon_class='fab fa-js-square',
            display_order=2,
            is_active=True
        )
        self.inactive_skill = JourneySkill.objects.create(
            roadmap_path=self.roadmap_path,
            name='Inactive Skill',
            icon_class='fas fa-times',
            display_order=3,
            is_active=False
        )
    
    def test_journey_skills_in_context(self):
        """Test that journey_skills is passed to template context"""
        response = self.client.get(reverse('roadmap:path_detail', kwargs={'slug': 'test-fullstack'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('journey_skills', response.context)
    
    def test_only_active_skills_in_context(self):
        """Test that only active journey skills are in context"""
        response = self.client.get(reverse('roadmap:path_detail', kwargs={'slug': 'test-fullstack'}))
        journey_skills = list(response.context['journey_skills'])
        self.assertEqual(len(journey_skills), 2)
        skill_names = [s.name for s in journey_skills]
        self.assertIn('Python', skill_names)
        self.assertIn('JavaScript', skill_names)
        self.assertNotIn('Inactive Skill', skill_names)
    
    def test_empty_journey_skills_no_error(self):
        """Test that empty journey skills doesn't cause errors"""
        # Create path with no journey skills
        empty_path = RoadmapPath.objects.create(
            name='Empty Path',
            slug='empty-path',
            subtitle='No skills',
            description='Path with no journey skills',
            icon_class='fas fa-question',
            difficulty='beginner',
            estimated_duration='1 month',
            order=2
        )
        # Create a phase so the path is valid
        RoadmapPhase.objects.create(
            roadmap_path=empty_path,
            name='Phase 1',
            description='Test phase',
            duration='1 month',
            order=1
        )
        
        response = self.client.get(reverse('roadmap:path_detail', kwargs={'slug': 'empty-path'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(response.context['journey_skills'])), 0)


# ============================================
# PROPERTY-BASED TESTS
# Feature: roadmap-skills-enhancement
# ============================================

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class JourneySkillPropertyTests(HypothesisTestCase):
    """
    Property-based tests for JourneySkill model
    Using hypothesis library for comprehensive testing
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up test roadmap path once for all tests"""
        super().setUpClass()
        # Use a unique slug to avoid conflicts
        import uuid
        cls.unique_slug = f'property-test-{uuid.uuid4().hex[:8]}'
    
    def setUp(self):
        """Set up test roadmap path"""
        # Clean up any existing path with this slug
        RoadmapPath.objects.filter(slug=self.unique_slug).delete()
        self.roadmap_path = RoadmapPath.objects.create(
            name=f'Property Test Path {self.unique_slug}',
            slug=self.unique_slug,
            subtitle='For property testing',
            description='Test path for property-based tests',
            icon_class='fas fa-flask',
            difficulty='intermediate',
            estimated_duration='6 months',
            order=99
        )
    
    @given(
        orders=st.lists(
            st.integers(min_value=0, max_value=1000),
            min_size=2,
            max_size=20,
            unique=True
        )
    )
    @settings(max_examples=100)
    def test_property_ordering(self, orders):
        """
        Property 1: Journey Skills Ordering
        
        *For any* set of JourneySkill objects with different display_order values
        belonging to the same RoadmapPath, querying with order_by('display_order')
        SHALL return them in ascending order by display_order.
        
        **Validates: Requirements 1.5, 3.2**
        Feature: roadmap-skills-enhancement, Property 1: Journey Skills Ordering
        """
        # Clean up any existing skills for this path
        JourneySkill.objects.filter(roadmap_path=self.roadmap_path).delete()
        
        # Create skills with random orders
        for i, order in enumerate(orders):
            JourneySkill.objects.create(
                roadmap_path=self.roadmap_path,
                name=f'Skill_{i}',
                icon_class='fas fa-code',
                display_order=order,
                is_active=True
            )
        
        # Query skills ordered by display_order
        skills = list(JourneySkill.objects.filter(
            roadmap_path=self.roadmap_path
        ).order_by('display_order'))
        
        # Verify ordering property: each skill's display_order should be <= next skill's
        for i in range(len(skills) - 1):
            self.assertLessEqual(
                skills[i].display_order,
                skills[i + 1].display_order,
                f"Skills not in ascending order: {skills[i].display_order} > {skills[i + 1].display_order}"
            )
    
    @given(
        active_count=st.integers(min_value=0, max_value=10),
        inactive_count=st.integers(min_value=0, max_value=10)
    )
    @settings(max_examples=100)
    def test_property_active_filtering(self, active_count, inactive_count):
        """
        Property 2: Active Skills Filtering
        
        *For any* RoadmapPath, querying JourneySkill objects with
        filter(roadmap_path=path, is_active=True) SHALL return only skills
        where is_active is True AND roadmap_path matches the given path.
        
        **Validates: Requirements 3.1**
        Feature: roadmap-skills-enhancement, Property 2: Active Skills Filtering
        """
        # Clean up any existing skills for this path
        JourneySkill.objects.filter(roadmap_path=self.roadmap_path).delete()
        
        # Create active skills
        for i in range(active_count):
            JourneySkill.objects.create(
                roadmap_path=self.roadmap_path,
                name=f'Active_Skill_{i}',
                icon_class='fas fa-check',
                display_order=i,
                is_active=True
            )
        
        # Create inactive skills
        for i in range(inactive_count):
            JourneySkill.objects.create(
                roadmap_path=self.roadmap_path,
                name=f'Inactive_Skill_{i}',
                icon_class='fas fa-times',
                display_order=active_count + i,
                is_active=False
            )
        
        # Query only active skills
        active_skills = JourneySkill.objects.filter(
            roadmap_path=self.roadmap_path,
            is_active=True
        )
        
        # Verify filtering property
        self.assertEqual(
            active_skills.count(),
            active_count,
            f"Expected {active_count} active skills, got {active_skills.count()}"
        )
        
        # Verify all returned skills are active
        for skill in active_skills:
            self.assertTrue(
                skill.is_active,
                f"Inactive skill {skill.name} returned in active filter"
            )
            self.assertEqual(
                skill.roadmap_path,
                self.roadmap_path,
                f"Skill {skill.name} has wrong roadmap_path"
            )
