"""
Role-Based Content System
=========================

Provides intelligent, role-aware default content for resumes.
This is the single source of truth for role-specific content.

Supported Roles:
- devops_sre: DevOps / SRE Engineer
- software_engineer: Software Engineer  
- ds_ml: Data Science / ML Engineer
- product_manager: Product Manager
- frontend: Frontend Developer
- backend: Backend Developer

Section Ordering:
- Education appears ABOVE Experience in all templates (industry standard)
"""

from typing import Dict, List, Any

# =============================================================================
# SECTION ORDERING - Single Source of Truth
# =============================================================================

# Standard section order for all resume templates
# Education comes before Experience (industry standard for most roles)
SECTION_ORDER = [
    'summary',
    'education',
    'experience',
    'skills',
    'languages',
    'certifications',
    'projects',
]

# =============================================================================
# ROLE DEFINITIONS
# =============================================================================

ROLE_OPTIONS = [
    ('devops_sre', 'DevOps / SRE Engineer'),
    ('software_engineer', 'Software Engineer'),
    ('ds_ml', 'DS / ML Engineer'),
    ('product_manager', 'Product Manager'),
    ('frontend', 'Frontend Developer'),
    ('backend', 'Backend Developer'),
]

ROLE_TITLES = {
    'devops_sre': 'Senior DevOps / SRE Engineer',
    'software_engineer': 'Senior Software Engineer',
    'ds_ml': 'Senior Data Scientist / ML Engineer',
    'product_manager': 'Senior Product Manager',
    'frontend': 'Senior Frontend Developer',
    'backend': 'Senior Backend Developer',
}

# =============================================================================
# ROLE-SPECIFIC SKILLS
# =============================================================================

ROLE_SKILLS = {
    'devops_sre': [
        'AWS', 'Azure', 'GCP',
        'Terraform', 'Terragrunt', 'CloudFormation',
        'Docker', 'Kubernetes', 'Helm',
        'Jenkins', 'GitHub Actions', 'GitLab CI/CD',
        'Ansible', 'Puppet', 'Chef',
        'Prometheus', 'Grafana', 'ELK Stack',
        'Python', 'Bash', 'Go',
        'Linux', 'Networking', 'Security',
    ],
    'software_engineer': [
        'Python', 'JavaScript', 'TypeScript',
        'Java', 'Go', 'C++',
        'React', 'Node.js', 'Django',
        'PostgreSQL', 'MongoDB', 'Redis',
        'REST APIs', 'GraphQL', 'gRPC',
        'Docker', 'Kubernetes', 'AWS',
        'Git', 'CI/CD', 'Agile',
        'System Design', 'Microservices',
    ],
    'ds_ml': [
        'Python', 'R', 'SQL',
        'TensorFlow', 'PyTorch', 'Scikit-learn',
        'Pandas', 'NumPy', 'Spark',
        'Deep Learning', 'NLP', 'Computer Vision',
        'MLflow', 'Kubeflow', 'SageMaker',
        'Statistics', 'A/B Testing',
        'Tableau', 'Power BI',
        'Feature Engineering', 'Model Deployment',
    ],
    'product_manager': [
        'Product Strategy', 'Roadmap Planning',
        'User Research', 'A/B Testing',
        'Agile/Scrum', 'JIRA', 'Confluence',
        'Data Analysis', 'SQL', 'Tableau',
        'Stakeholder Management',
        'Go-to-Market Strategy',
        'Competitive Analysis',
        'User Stories', 'PRDs',
        'Figma', 'Miro',
    ],
    'frontend': [
        'JavaScript', 'TypeScript', 'HTML5', 'CSS3',
        'React', 'Vue.js', 'Angular',
        'Next.js', 'Nuxt.js',
        'Tailwind CSS', 'Sass', 'Styled Components',
        'Redux', 'Zustand', 'React Query',
        'Jest', 'Cypress', 'Playwright',
        'Webpack', 'Vite', 'ESLint',
        'Responsive Design', 'Accessibility',
    ],
    'backend': [
        'Python', 'Java', 'Go', 'Node.js',
        'Django', 'FastAPI', 'Spring Boot',
        'PostgreSQL', 'MySQL', 'MongoDB',
        'Redis', 'Elasticsearch', 'Kafka',
        'REST APIs', 'GraphQL', 'gRPC',
        'Docker', 'Kubernetes', 'AWS',
        'Microservices', 'Event-Driven Architecture',
        'System Design', 'Performance Optimization',
    ],
}

# =============================================================================
# ROLE-SPECIFIC SUMMARIES
# =============================================================================

ROLE_SUMMARIES = {
    'devops_sre': """Results-driven DevOps/SRE Engineer with 5+ years of experience designing and implementing scalable cloud infrastructure, CI/CD pipelines, and observability solutions. Expert in AWS, Kubernetes, Terraform, and GitOps practices. Proven track record of reducing deployment times by 70%, achieving 99.9% uptime SLAs, and implementing infrastructure-as-code across multi-cloud environments. Passionate about automation, reliability engineering, and enabling development teams to ship faster with confidence.""",
    
    'software_engineer': """Senior Software Engineer with 5+ years of experience building scalable, high-performance applications. Proficient in full-stack development with expertise in Python, JavaScript, and cloud-native architectures. Strong background in system design, API development, and microservices. Committed to writing clean, maintainable code and implementing best practices in software development lifecycle. Track record of delivering impactful features that drive business growth.""",
    
    'ds_ml': """Data Scientist / ML Engineer with 5+ years of experience developing and deploying machine learning models at scale. Expert in Python, TensorFlow, and PyTorch with a strong foundation in statistical analysis and data engineering. Proven ability to translate business requirements into ML solutions, achieving significant improvements in prediction accuracy and operational efficiency. Experienced in MLOps practices and end-to-end ML pipeline development.""",
    
    'product_manager': """Strategic Product Manager with 5+ years of experience driving product vision and execution for B2B SaaS platforms. Skilled in translating customer needs into product requirements, prioritizing roadmaps, and collaborating with cross-functional teams. Track record of launching products that increased revenue by 40% and improved user engagement by 60%. Data-driven decision maker with strong technical background and excellent stakeholder management skills.""",
    
    'frontend': """Senior Frontend Developer with 5+ years of experience building responsive, accessible, and performant web applications. Expert in React, TypeScript, and modern CSS frameworks. Passionate about user experience, component architecture, and frontend performance optimization. Strong advocate for accessibility standards and best practices. Experience leading frontend teams and establishing coding standards.""",
    
    'backend': """Senior Backend Developer with 5+ years of experience designing and implementing scalable distributed systems. Expert in Python, Go, and cloud-native architectures. Strong background in API design, database optimization, and microservices. Proven track record of building systems handling millions of requests daily with 99.99% uptime. Passionate about clean architecture, performance optimization, and mentoring junior developers.""",
}

# =============================================================================
# ROLE-SPECIFIC EXPERIENCE TEMPLATES
# =============================================================================

ROLE_EXPERIENCE = {
    'devops_sre': {
        'role': 'Senior DevOps Engineer',
        'company': 'Tech Company',
        'start_date': '2022',
        'end_date': 'Present',
        'bullets': [
            'Architected and implemented multi-region Kubernetes clusters on AWS EKS, achieving 99.99% uptime and supporting 500+ microservices',
            'Designed and deployed GitOps-based CI/CD pipelines using GitHub Actions and ArgoCD, reducing deployment time from 2 hours to 15 minutes',
            'Implemented Infrastructure as Code using Terraform and Terragrunt, managing 200+ AWS resources across 5 environments',
            'Built comprehensive observability stack with Prometheus, Grafana, and ELK, reducing MTTR by 60%',
            'Led security hardening initiatives including IAM policies, WAF rules, and secrets management with HashiCorp Vault',
        ]
    },
    'software_engineer': {
        'role': 'Senior Software Engineer',
        'company': 'Tech Company',
        'start_date': '2022',
        'end_date': 'Present',
        'bullets': [
            'Designed and implemented RESTful APIs serving 10M+ daily requests with 99.9% availability',
            'Led migration from monolithic architecture to microservices, improving scalability and deployment frequency by 5x',
            'Optimized database queries and implemented caching strategies, reducing API response times by 40%',
            'Mentored team of 5 junior developers and conducted code reviews to maintain high code quality standards',
            'Implemented comprehensive test coverage achieving 85%+ code coverage across all services',
        ]
    },
    'ds_ml': {
        'role': 'Senior ML Engineer',
        'company': 'Tech Company',
        'start_date': '2022',
        'end_date': 'Present',
        'bullets': [
            'Developed and deployed production ML models serving 5M+ predictions daily with 99.5% uptime',
            'Built end-to-end ML pipelines using Airflow and MLflow, reducing model deployment time by 70%',
            'Implemented A/B testing framework for ML models, enabling data-driven model selection and improving conversion by 25%',
            'Optimized model inference latency from 200ms to 50ms through model quantization and optimization techniques',
            'Collaborated with product teams to translate business requirements into ML solutions driving $2M+ annual revenue',
        ]
    },
    'product_manager': {
        'role': 'Senior Product Manager',
        'company': 'Tech Company',
        'start_date': '2022',
        'end_date': 'Present',
        'bullets': [
            'Led product strategy and roadmap for B2B SaaS platform serving 500+ enterprise customers',
            'Launched 3 major product features that increased ARR by 40% and reduced churn by 25%',
            'Conducted 100+ customer interviews and synthesized insights into actionable product requirements',
            'Collaborated with engineering, design, and marketing teams to deliver products on time and within budget',
            'Established data-driven decision framework using analytics and A/B testing, improving feature adoption by 60%',
        ]
    },
    'frontend': {
        'role': 'Senior Frontend Developer',
        'company': 'Tech Company',
        'start_date': '2022',
        'end_date': 'Present',
        'bullets': [
            'Led frontend architecture for React-based SaaS platform serving 100K+ daily active users',
            'Implemented design system and component library, reducing development time by 40% and ensuring UI consistency',
            'Optimized Core Web Vitals achieving 95+ Lighthouse scores, improving SEO rankings and user engagement',
            'Established frontend testing strategy with Jest and Cypress, achieving 90%+ code coverage',
            'Mentored team of 4 developers and conducted code reviews to maintain high code quality standards',
        ]
    },
    'backend': {
        'role': 'Senior Backend Developer',
        'company': 'Tech Company',
        'start_date': '2022',
        'end_date': 'Present',
        'bullets': [
            'Designed and implemented microservices architecture handling 50M+ daily API requests with sub-100ms latency',
            'Built event-driven systems using Kafka and Redis, enabling real-time data processing and notifications',
            'Optimized PostgreSQL queries and implemented read replicas, reducing database load by 60%',
            'Led API design and documentation efforts, improving developer experience and reducing integration time',
            'Implemented comprehensive monitoring and alerting, reducing incident response time by 70%',
        ]
    },
}

# =============================================================================
# PUBLIC API
# =============================================================================

def get_role_title(role: str) -> str:
    """Get the display title for a role."""
    return ROLE_TITLES.get(role, 'Software Professional')


def get_role_skills(role: str) -> List[str]:
    """Get default skills for a role."""
    return ROLE_SKILLS.get(role, ROLE_SKILLS['software_engineer'])


def get_role_summary(role: str) -> str:
    """Get default professional summary for a role."""
    return ROLE_SUMMARIES.get(role, ROLE_SUMMARIES['software_engineer'])


def get_role_experience(role: str) -> Dict[str, Any]:
    """Get default experience entry for a role."""
    return ROLE_EXPERIENCE.get(role, ROLE_EXPERIENCE['software_engineer'])


def get_role_content(role: str) -> Dict[str, Any]:
    """
    Get all role-specific content in one call.
    This is the main API for role-based content.
    """
    return {
        'role': role,
        'role_title': get_role_title(role),
        'skills': get_role_skills(role),
        'summary': get_role_summary(role),
        'experience': get_role_experience(role),
    }


def get_all_roles() -> List[tuple]:
    """Get all available role options."""
    return ROLE_OPTIONS


def get_section_order() -> List[str]:
    """
    Get the standard section order for resumes.
    Education appears before Experience (industry standard).
    """
    return SECTION_ORDER.copy()
