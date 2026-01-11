# Generated migration to populate initial Journey Skills
from django.db import migrations


def populate_journey_skills(apps, schema_editor):
    """Populate initial journey skills for all roadmap paths"""
    RoadmapPath = apps.get_model('roadmap', 'RoadmapPath')
    JourneySkill = apps.get_model('roadmap', 'JourneySkill')
    
    # DevOps/SRE Skills
    devops_skills = [
        ('AWS', 'fab fa-aws', 1),
        ('Azure', 'fab fa-microsoft', 2),
        ('GCP', 'fab fa-google', 3),
        ('DigitalOcean', 'fab fa-digital-ocean', 4),
        ('AWS Migration', 'fas fa-cloud-upload-alt', 5),
        ('Terraform', 'fas fa-cubes', 6),
        ('Terragrunt', 'fas fa-layer-group', 7),
        ('Shell Scripting', 'fas fa-terminal', 8),
        ('Docker', 'fab fa-docker', 9),
        ('Kubernetes', 'fas fa-dharmachakra', 10),
        ('Jenkins', 'fab fa-jenkins', 11),
        ('Ansible', 'fas fa-cogs', 12),
        ('Puppet', 'fas fa-theater-masks', 13),
        ('Packer', 'fas fa-box', 14),
        ('Python', 'fab fa-python', 15),
        ('Git', 'fab fa-git-alt', 16),
        ('GitHub', 'fab fa-github', 17),
        ('Bitbucket', 'fab fa-bitbucket', 18),
        ('GitLab', 'fab fa-gitlab', 19),
        ('Bamboo', 'fas fa-seedling', 20),
        ('GitLab CI/CD', 'fas fa-sync-alt', 21),
        ('GitHub Actions', 'fas fa-play-circle', 22),
    ]
    
    # Full-Stack Development Skills
    fullstack_skills = [
        ('Python', 'fab fa-python', 1),
        ('JavaScript', 'fab fa-js-square', 2),
        ('TypeScript', 'fas fa-code', 3),
        ('Java', 'fab fa-java', 4),
        ('Go', 'fas fa-gopuram', 5),
        ('React', 'fab fa-react', 6),
        ('Vue.js', 'fab fa-vuejs', 7),
        ('Node.js', 'fab fa-node-js', 8),
        ('Django', 'fas fa-leaf', 9),
        ('FastAPI', 'fas fa-bolt', 10),
        ('PostgreSQL', 'fas fa-database', 11),
        ('MySQL', 'fas fa-database', 12),
        ('MongoDB', 'fas fa-leaf', 13),
        ('Redis', 'fas fa-memory', 14),
        ('REST APIs', 'fas fa-plug', 15),
        ('GraphQL', 'fas fa-project-diagram', 16),
        ('Docker', 'fab fa-docker', 17),
        ('Kubernetes', 'fas fa-dharmachakra', 18),
        ('Git', 'fab fa-git-alt', 19),
        ('CI/CD', 'fas fa-sync-alt', 20),
        ('AWS', 'fab fa-aws', 21),
        ('System Design', 'fas fa-sitemap', 22),
    ]
    
    # Data Science & Machine Learning Skills
    dsml_skills = [
        ('Python', 'fab fa-python', 1),
        ('R', 'fab fa-r-project', 2),
        ('SQL', 'fas fa-database', 3),
        ('Scala', 'fas fa-code', 4),
        ('TensorFlow', 'fas fa-brain', 5),
        ('PyTorch', 'fas fa-fire', 6),
        ('Scikit-learn', 'fas fa-project-diagram', 7),
        ('Keras', 'fas fa-network-wired', 8),
        ('Pandas', 'fas fa-table', 9),
        ('NumPy', 'fas fa-calculator', 10),
        ('Spark', 'fas fa-bolt', 11),
        ('Airflow', 'fas fa-wind', 12),
        ('AWS SageMaker', 'fab fa-aws', 13),
        ('MLflow', 'fas fa-flask', 14),
        ('Docker', 'fab fa-docker', 15),
        ('Matplotlib', 'fas fa-chart-line', 16),
        ('Seaborn', 'fas fa-chart-area', 17),
        ('Tableau', 'fas fa-chart-pie', 18),
        ('PostgreSQL', 'fas fa-database', 19),
        ('MongoDB', 'fas fa-leaf', 20),
        ('BigQuery', 'fab fa-google', 21),
    ]
    
    # Map slug patterns to skills
    skill_mapping = {
        'devops': devops_skills,
        'full-stack': fullstack_skills,
        'data-science': dsml_skills,
    }
    
    # Get all roadmap paths and create skills
    for path in RoadmapPath.objects.all():
        skills_to_create = None
        slug_lower = path.slug.lower()
        
        # Match path to skills based on slug
        if 'devops' in slug_lower or 'sre' in slug_lower:
            skills_to_create = devops_skills
        elif 'full-stack' in slug_lower or 'fullstack' in slug_lower:
            skills_to_create = fullstack_skills
        elif 'data-science' in slug_lower or 'machine-learning' in slug_lower or 'dsml' in slug_lower:
            skills_to_create = dsml_skills
        
        if skills_to_create:
            for name, icon_class, order in skills_to_create:
                JourneySkill.objects.create(
                    roadmap_path=path,
                    name=name,
                    icon_class=icon_class,
                    display_order=order,
                    is_active=True
                )


def reverse_journey_skills(apps, schema_editor):
    """Remove all journey skills"""
    JourneySkill = apps.get_model('roadmap', 'JourneySkill')
    JourneySkill.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0002_add_journey_skill_model'),
    ]

    operations = [
        migrations.RunPython(populate_journey_skills, reverse_journey_skills),
    ]
