from django.contrib import admin
from .models import RoadmapPath, RoadmapPhase, RoadmapSkill, UserProgress, RoadmapHighlight


class RoadmapHighlightInline(admin.TabularInline):
    model = RoadmapHighlight
    extra = 1
    fields = ('title', 'icon_class', 'order')


class RoadmapSkillInline(admin.TabularInline):
    model = RoadmapSkill
    extra = 1
    fields = ('name', 'description', 'is_core', 'order')


class RoadmapPhaseInline(admin.StackedInline):
    model = RoadmapPhase
    extra = 0
    fields = ('name', 'description', 'duration', 'order', 'is_active')


@admin.register(RoadmapPath)
class RoadmapPathAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'estimated_duration', 'order', 'is_active', 'created_at')
    list_filter = ('difficulty', 'is_active', 'created_at')
    search_fields = ('name', 'subtitle', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'subtitle', 'description')
        }),
        ('Display Settings', {
            'fields': ('icon_class', 'difficulty', 'estimated_duration', 'order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    inlines = [RoadmapHighlightInline, RoadmapPhaseInline]


@admin.register(RoadmapPhase)
class RoadmapPhaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'roadmap_path', 'duration', 'order', 'is_active')
    list_filter = ('roadmap_path', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('roadmap_path', 'order')
    
    inlines = [RoadmapSkillInline]


@admin.register(RoadmapSkill)
class RoadmapSkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'phase', 'is_core', 'order')
    list_filter = ('phase__roadmap_path', 'phase', 'is_core')
    search_fields = ('name', 'description')
    ordering = ('phase__roadmap_path', 'phase__order', 'order')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'roadmap_path', 'skill', 'status', 'updated_at')
    list_filter = ('status', 'roadmap_path', 'updated_at')
    search_fields = ('user__username', 'user__email', 'skill__name')
    ordering = ('-updated_at',)
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(RoadmapHighlight)
class RoadmapHighlightAdmin(admin.ModelAdmin):
    list_display = ('title', 'roadmap_path', 'icon_class', 'order')
    list_filter = ('roadmap_path',)
    search_fields = ('title',)
    ordering = ('roadmap_path', 'order')