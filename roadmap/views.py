from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_headers
from django.utils import timezone
from .models import RoadmapPath, RoadmapPhase, UserProgress, JourneySkill, JourneySkillProgress


@never_cache
@vary_on_headers('User-Agent')
def home(request):
    """
    Roadmap home page with career transition explanation and interactive roadmap cards
    """
    # Get all active roadmap paths ordered by their sequence
    roadmap_paths = RoadmapPath.objects.filter(is_active=True).order_by('order').prefetch_related('highlights')
    
    # Get user progress if authenticated
    user_progress = {}
    if request.user.is_authenticated:
        progress_data = UserProgress.objects.filter(
            user=request.user
        ).select_related('roadmap_path', 'skill')
        
        for progress in progress_data:
            path_slug = progress.roadmap_path.slug
            if path_slug not in user_progress:
                user_progress[path_slug] = {
                    'total_skills': 0,
                    'completed_skills': 0,
                    'in_progress_skills': 0
                }
            
            user_progress[path_slug]['total_skills'] += 1
            if progress.status == 'completed':
                user_progress[path_slug]['completed_skills'] += 1
            elif progress.status == 'in_progress':
                user_progress[path_slug]['in_progress_skills'] += 1
    
    context = {
        'roadmap_paths': roadmap_paths,
        'user_progress': user_progress,
        'page_type': 'roadmap_home',  # For state isolation
    }
    
    return render(request, 'roadmap/home.html', context)


@never_cache
@vary_on_headers('User-Agent')
def path_detail(request, slug):
    """
    Individual roadmap path detail page with proper state isolation
    """
    roadmap_path = get_object_or_404(RoadmapPath, slug=slug, is_active=True)
    phases = roadmap_path.phases.filter(is_active=True).prefetch_related('skills').order_by('order')
    
    # Calculate total skills count
    total_skills = 0
    for phase in phases:
        total_skills += phase.skills.count()
    
    # Get user progress for this path if authenticated
    user_progress = {}
    completed_count = 0
    in_progress_count = 0
    
    if request.user.is_authenticated:
        progress_data = UserProgress.objects.filter(
            user=request.user,
            roadmap_path=roadmap_path
        ).select_related('skill')
        
        for progress in progress_data:
            if progress.skill:
                user_progress[progress.skill.id] = progress.status
                if progress.status == 'completed':
                    completed_count += 1
                elif progress.status == 'in_progress':
                    in_progress_count += 1
    
    remaining_count = total_skills - completed_count - in_progress_count
    
    # Get journey tools for "Start Your Journey" section
    journey_skills = JourneySkill.objects.filter(
        roadmap_path=roadmap_path,
        is_active=True
    ).order_by('display_order')
    
    # Get journey skill progress for authenticated users
    journey_skill_progress = {}
    journey_completed_count = 0
    journey_in_progress_count = 0
    
    if request.user.is_authenticated:
        progress_data = JourneySkillProgress.objects.filter(
            user=request.user,
            journey_skill__roadmap_path=roadmap_path
        ).select_related('journey_skill')
        
        for progress in progress_data:
            journey_skill_progress[progress.journey_skill.id] = progress.status
            if progress.status == 'completed':
                journey_completed_count += 1
            elif progress.status == 'in_progress':
                journey_in_progress_count += 1
    
    journey_total = journey_skills.count()
    journey_remaining = journey_total - journey_completed_count - journey_in_progress_count
    
    context = {
        'roadmap_path': roadmap_path,
        'phases': phases,
        'user_progress': user_progress,
        'total_skills': total_skills,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'remaining_count': remaining_count,
        'journey_skills': journey_skills,
        'journey_skill_progress': journey_skill_progress,
        'journey_total': journey_total,
        'journey_completed_count': journey_completed_count,
        'journey_in_progress_count': journey_in_progress_count,
        'journey_remaining': journey_remaining,
        'page_type': 'roadmap_detail',
        'path_slug': slug,
    }
    
    return render(request, 'roadmap/path_detail.html', context)


def api_path_detail(request, slug):
    """
    API endpoint to get roadmap path details for AJAX requests
    """
    roadmap_path = get_object_or_404(RoadmapPath, slug=slug, is_active=True)
    phases = roadmap_path.phases.filter(is_active=True).prefetch_related('skills')
    
    # Build the response data
    phases_data = []
    for phase in phases:
        skills_data = []
        for skill in phase.skills.all():
            skills_data.append({
                'id': skill.id,
                'name': skill.name,
                'description': skill.description,
                'is_core': skill.is_core,
                'order': skill.order,
            })
        
        phases_data.append({
            'id': phase.id,
            'name': phase.name,
            'description': phase.description,
            'duration': phase.duration,
            'order': phase.order,
            'skills': skills_data,
        })
    
    # Get highlights
    highlights_data = []
    for highlight in roadmap_path.highlights.all():
        highlights_data.append({
            'title': highlight.title,
            'icon_class': highlight.icon_class,
            'order': highlight.order,
        })
    
    data = {
        'id': roadmap_path.id,
        'name': roadmap_path.name,
        'subtitle': roadmap_path.subtitle,
        'description': roadmap_path.description,
        'icon_class': roadmap_path.icon_class,
        'difficulty': roadmap_path.difficulty,
        'estimated_duration': roadmap_path.estimated_duration,
        'phases': phases_data,
        'highlights': highlights_data,
    }
    
    return JsonResponse(data)


@login_required
def update_progress(request, skill_id):
    """
    Update user progress for a specific skill
    """
    if request.method == 'POST':
        from .models import RoadmapSkill
        skill = get_object_or_404(RoadmapSkill, id=skill_id)
        status = request.POST.get('status', 'not_started')
        
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            roadmap_path=skill.phase.roadmap_path,
            skill=skill,
            defaults={'status': status}
        )
        
        if not created:
            progress.status = status
            progress.save()
        
        return JsonResponse({'success': True, 'status': status})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def update_journey_skill_progress(request, skill_id):
    """
    Update user progress for a journey skill (Start Your Journey section).
    Cycles through: not_started -> in_progress -> completed -> not_started
    """
    if request.method == 'POST':
        journey_skill = get_object_or_404(JourneySkill, id=skill_id, is_active=True)
        
        # Get or create progress record
        progress, created = JourneySkillProgress.objects.get_or_create(
            user=request.user,
            journey_skill=journey_skill,
            defaults={'status': 'not_started'}
        )
        
        # Determine new status (cycle through states)
        current_status = progress.status
        if current_status == 'not_started':
            new_status = 'in_progress'
            progress.started_at = timezone.now()
        elif current_status == 'in_progress':
            new_status = 'completed'
            progress.completed_at = timezone.now()
        else:  # completed
            new_status = 'not_started'
            progress.started_at = None
            progress.completed_at = None
        
        progress.status = new_status
        progress.save()
        
        # Calculate updated counts for this roadmap path
        all_progress = JourneySkillProgress.objects.filter(
            user=request.user,
            journey_skill__roadmap_path=journey_skill.roadmap_path
        )
        completed_count = all_progress.filter(status='completed').count()
        in_progress_count = all_progress.filter(status='in_progress').count()
        total_count = JourneySkill.objects.filter(
            roadmap_path=journey_skill.roadmap_path,
            is_active=True
        ).count()
        
        return JsonResponse({
            'success': True,
            'status': new_status,
            'skill_id': skill_id,
            'completed_count': completed_count,
            'in_progress_count': in_progress_count,
            'total_count': total_count,
            'remaining_count': total_count - completed_count - in_progress_count
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
