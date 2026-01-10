from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import RoadmapPath, RoadmapPhase, UserProgress


def home(request):
    """
    Roadmap home page with career transition explanation and interactive roadmap cards
    """
    # Get all active roadmap paths ordered by their sequence
    roadmap_paths = RoadmapPath.objects.filter(is_active=True).order_by('order')
    
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
    }
    
    return render(request, 'roadmap/home.html', context)


def path_detail(request, slug):
    """
    Individual roadmap path detail page
    """
    roadmap_path = get_object_or_404(RoadmapPath, slug=slug, is_active=True)
    phases = roadmap_path.phases.filter(is_active=True).prefetch_related('skills')
    
    # Get user progress for this path if authenticated
    user_progress = {}
    if request.user.is_authenticated:
        progress_data = UserProgress.objects.filter(
            user=request.user,
            roadmap_path=roadmap_path
        ).select_related('skill')
        
        for progress in progress_data:
            if progress.skill:
                user_progress[progress.skill.id] = progress.status
    
    context = {
        'roadmap_path': roadmap_path,
        'phases': phases,
        'user_progress': user_progress,
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