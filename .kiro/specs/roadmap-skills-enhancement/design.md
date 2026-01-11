# Design Document: Roadmap Skills Enhancement

## Overview

This design document describes the implementation of dynamic skill chips in the "Start Your Journey" section of roadmap path detail pages. The feature introduces a new `JourneySkill` model that is managed through Django Admin and rendered dynamically in the template with subtle CSS animations.

The design follows Django best practices and integrates seamlessly with the existing roadmap application structure without modifying any existing components.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Django Admin                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  JourneySkillAdmin                                       │    │
│  │  - List display with filters                             │    │
│  │  - Inline editing                                        │    │
│  │  - Search by name                                        │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Database Layer                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  JourneySkill Model                                      │    │
│  │  - name: CharField                                       │    │
│  │  - icon_class: CharField                                 │    │
│  │  - roadmap_path: ForeignKey(RoadmapPath)                │    │
│  │  - display_order: PositiveIntegerField                   │    │
│  │  - is_active: BooleanField                               │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        View Layer                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  path_detail(request, slug)                              │    │
│  │  - Query JourneySkill.objects.filter(                    │    │
│  │      roadmap_path=roadmap_path, is_active=True           │    │
│  │    ).order_by('display_order')                           │    │
│  │  - Add 'journey_skills' to context                       │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Template Layer                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  path_detail.html                                        │    │
│  │  - "Start Your Journey" section enhanced                 │    │
│  │  - {% for skill in journey_skills %}                     │    │
│  │  - Skill chip component with icon + name                 │    │
│  │  - CSS animations (fade-in, stagger, hover)              │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. JourneySkill Model

```python
class JourneySkill(models.Model):
    """
    Represents skills displayed in the 'Start Your Journey' section.
    Separate from RoadmapSkill which is tied to phases.
    """
    roadmap_path = models.ForeignKey(
        RoadmapPath, 
        on_delete=models.CASCADE, 
        related_name='journey_skills'
    )
    name = models.CharField(max_length=100)
    icon_class = models.CharField(
        max_length=100, 
        default='fas fa-code',
        help_text='Font Awesome icon class (e.g., fab fa-aws, fas fa-docker)'
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['roadmap_path', 'display_order']
        verbose_name = 'Journey Skill'
        verbose_name_plural = 'Journey Skills'
    
    def __str__(self):
        return f"{self.roadmap_path.name} - {self.name}"
```

### 2. Admin Configuration

```python
class JourneySkillInline(admin.TabularInline):
    model = JourneySkill
    extra = 1
    fields = ('name', 'icon_class', 'display_order', 'is_active')

@admin.register(JourneySkill)
class JourneySkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'roadmap_path', 'icon_class', 'display_order', 'is_active')
    list_filter = ('roadmap_path', 'is_active')
    search_fields = ('name',)
    list_editable = ('display_order', 'is_active')
    ordering = ('roadmap_path', 'display_order')
```

### 3. View Integration

The `path_detail` view will be updated to include journey skills in the context:

```python
def path_detail(request, slug):
    roadmap_path = get_object_or_404(RoadmapPath, slug=slug, is_active=True)
    # ... existing code ...
    
    # Query journey skills for this path
    journey_skills = JourneySkill.objects.filter(
        roadmap_path=roadmap_path,
        is_active=True
    ).order_by('display_order')
    
    context = {
        # ... existing context ...
        'journey_skills': journey_skills,
    }
    return render(request, 'roadmap/path_detail.html', context)
```

### 4. Template Component

The skill chip component structure:

```html
{% if journey_skills %}
<div class="journey-skills-container">
    <div class="journey-skills-grid">
        {% for skill in journey_skills %}
        <div class="journey-skill-chip" style="--animation-delay: {{ forloop.counter0 }}">
            <i class="{{ skill.icon_class }}"></i>
            <span>{{ skill.name }}</span>
        </div>
        {% endfor %}
    </div>
</div>
{% endif %}
```

## Data Models

### JourneySkill Entity

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated ID |
| roadmap_path | ForeignKey | NOT NULL, CASCADE | Reference to RoadmapPath |
| name | CharField(100) | NOT NULL | Skill name (e.g., "Docker") |
| icon_class | CharField(100) | DEFAULT 'fas fa-code' | Font Awesome class |
| display_order | PositiveIntegerField | DEFAULT 0 | Rendering order |
| is_active | BooleanField | DEFAULT True | Visibility toggle |
| created_at | DateTimeField | auto_now_add | Creation timestamp |
| updated_at | DateTimeField | auto_now | Last update timestamp |

### Initial Data (Migration)

**DevOps/SRE Path:**
| Name | Icon Class | Order |
|------|------------|-------|
| AWS | fab fa-aws | 1 |
| Azure | fab fa-microsoft | 2 |
| GCP | fab fa-google | 3 |
| DigitalOcean | fab fa-digital-ocean | 4 |
| AWS Migration | fas fa-cloud-upload-alt | 5 |
| Terraform | fas fa-cubes | 6 |
| Terragrunt | fas fa-layer-group | 7 |
| Shell Scripting | fas fa-terminal | 8 |
| Docker | fab fa-docker | 9 |
| Kubernetes | fas fa-dharmachakra | 10 |
| Jenkins | fab fa-jenkins | 11 |
| Ansible | fas fa-cogs | 12 |
| Puppet | fas fa-puppet | 13 |
| Packer | fas fa-box | 14 |
| Python | fab fa-python | 15 |
| Git | fab fa-git-alt | 16 |
| GitHub | fab fa-github | 17 |
| Bitbucket | fab fa-bitbucket | 18 |
| GitLab | fab fa-gitlab | 19 |
| Bamboo | fas fa-seedling | 20 |
| GitLab CI/CD | fas fa-sync-alt | 21 |
| GitHub Actions | fas fa-play-circle | 22 |

**Full-Stack Development Path:**
| Name | Icon Class | Order |
|------|------------|-------|
| Python | fab fa-python | 1 |
| JavaScript | fab fa-js-square | 2 |
| TypeScript | fas fa-code | 3 |
| Java | fab fa-java | 4 |
| Go | fas fa-gopuram | 5 |
| React | fab fa-react | 6 |
| Vue.js | fab fa-vuejs | 7 |
| Node.js | fab fa-node-js | 8 |
| Django | fas fa-leaf | 9 |
| FastAPI | fas fa-bolt | 10 |
| PostgreSQL | fas fa-database | 11 |
| MySQL | fas fa-database | 12 |
| MongoDB | fas fa-leaf | 13 |
| Redis | fas fa-memory | 14 |
| REST APIs | fas fa-plug | 15 |
| GraphQL | fas fa-project-diagram | 16 |
| Docker | fab fa-docker | 17 |
| Kubernetes | fas fa-dharmachakra | 18 |
| Git | fab fa-git-alt | 19 |
| CI/CD | fas fa-sync-alt | 20 |
| AWS | fab fa-aws | 21 |
| System Design | fas fa-sitemap | 22 |

**Data Science/ML Path:**
| Name | Icon Class | Order |
|------|------------|-------|
| Python | fab fa-python | 1 |
| R | fab fa-r-project | 2 |
| SQL | fas fa-database | 3 |
| Scala | fas fa-code | 4 |
| TensorFlow | fas fa-brain | 5 |
| PyTorch | fas fa-fire | 6 |
| Scikit-learn | fas fa-project-diagram | 7 |
| Keras | fas fa-network-wired | 8 |
| Pandas | fas fa-table | 9 |
| NumPy | fas fa-calculator | 10 |
| Spark | fas fa-bolt | 11 |
| Airflow | fas fa-wind | 12 |
| AWS SageMaker | fab fa-aws | 13 |
| MLflow | fas fa-flask | 14 |
| Docker | fab fa-docker | 15 |
| Matplotlib | fas fa-chart-line | 16 |
| Seaborn | fas fa-chart-area | 17 |
| Tableau | fas fa-chart-pie | 18 |
| PostgreSQL | fas fa-database | 19 |
| MongoDB | fas fa-leaf | 20 |
| BigQuery | fab fa-google | 21 |

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Journey Skills Ordering

*For any* set of JourneySkill objects with different display_order values belonging to the same RoadmapPath, querying with `order_by('display_order')` SHALL return them in ascending order by display_order.

**Validates: Requirements 1.5, 3.2**

### Property 2: Active Skills Filtering

*For any* RoadmapPath, querying JourneySkill objects with `filter(roadmap_path=path, is_active=True)` SHALL return only skills where is_active is True AND roadmap_path matches the given path.

**Validates: Requirements 3.1**

## Error Handling

### Database Errors

- **Missing RoadmapPath**: If a JourneySkill references a deleted RoadmapPath, CASCADE delete will remove the skill automatically
- **Duplicate display_order**: Allowed - skills with same order will be sorted by secondary criteria (id)

### View Errors

- **No skills found**: Return empty queryset, template handles gracefully with `{% if journey_skills %}`
- **Invalid roadmap path**: Handled by existing 404 logic in path_detail view

### Template Errors

- **Missing icon_class**: Default value 'fas fa-code' ensures icon always renders
- **Empty name**: CharField is required, Django validation prevents empty names

## Testing Strategy

### Unit Tests

Unit tests will verify specific examples and edge cases:

1. **Model Tests**
   - JourneySkill creation with all required fields
   - JourneySkill string representation
   - Default values (icon_class, display_order, is_active)

2. **View Tests**
   - Context contains 'journey_skills' key
   - Empty queryset when no skills exist for path
   - Skills filtered by roadmap_path correctly

3. **Migration Tests**
   - Initial skills created for all three paths
   - Skills have correct icons and display_order

### Property-Based Tests

Property-based tests will use the `hypothesis` library to verify universal properties:

1. **Ordering Property Test**
   - Generate random JourneySkill objects with various display_order values
   - Verify query results are always in ascending order
   - Minimum 100 iterations

2. **Filtering Property Test**
   - Generate random skills with mixed is_active values
   - Verify filter returns only active skills for correct path
   - Minimum 100 iterations

### Test Configuration

- Framework: Django TestCase + pytest
- Property testing: hypothesis library
- Minimum iterations: 100 per property test
- Tag format: **Feature: roadmap-skills-enhancement, Property N: [description]**
