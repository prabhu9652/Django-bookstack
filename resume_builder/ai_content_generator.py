"""
Enterprise-Grade AI Content Generator for Resume Builder
Provides role-specific, ATS-optimized content generation for resumes and cover letters.

Features:
- Role-specific bullet point generation (DevOps/SRE, Software Engineer, DS/ML)
- ATS keyword optimization
- Impact-driven achievement formatting
- Multiple content variants per role
- Cover letter generation matching resume content
"""

import re
import random
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ContentSuggestion:
    """Represents a content suggestion with metadata"""
    text: str
    keywords: List[str]
    impact_score: float  # 0-1 score for ATS impact
    category: str  # skill_category this relates to


# ============================================================================
# ROLE-SPECIFIC SKILL DATABASES
# ============================================================================

ROLE_SKILLS = {
    'devops_sre': {
        'cloud_platforms': ['AWS', 'Azure', 'GCP', 'DigitalOcean', 'Oracle Cloud'],
        'containerization': ['Docker', 'Kubernetes', 'EKS', 'AKS', 'GKE', 'OpenShift', 'Rancher'],
        'iac': ['Terraform', 'Terragrunt', 'CloudFormation', 'Pulumi', 'Ansible', 'Chef', 'Puppet'],
        'cicd': ['GitHub Actions', 'GitLab CI/CD', 'Jenkins', 'ArgoCD', 'CircleCI', 'Azure DevOps'],
        'monitoring': ['Prometheus', 'Grafana', 'Datadog', 'New Relic', 'CloudWatch', 'ELK Stack'],
        'scripting': ['Python', 'Bash', 'Go', 'PowerShell'],
        'security': ['HashiCorp Vault', 'AWS IAM', 'RBAC', 'SOC2', 'SAST/DAST'],
    },
    'software_engineer': {
        'languages': ['Python', 'JavaScript', 'TypeScript', 'Java', 'Go', 'Rust', 'C++'],
        'frontend': ['React', 'Vue.js', 'Angular', 'Next.js', 'Tailwind CSS'],
        'backend': ['Node.js', 'Django', 'FastAPI', 'Spring Boot', 'Express.js'],
        'databases': ['PostgreSQL', 'MongoDB', 'Redis', 'MySQL', 'DynamoDB'],
        'architecture': ['Microservices', 'REST APIs', 'GraphQL', 'Event-Driven', 'CQRS'],
        'testing': ['Jest', 'Pytest', 'Cypress', 'Selenium', 'TDD/BDD'],
    },
    'ds_ml': {
        'ml_frameworks': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'XGBoost', 'LightGBM'],
        'data_tools': ['Pandas', 'NumPy', 'Spark', 'Dask', 'SQL', 'Airflow'],
        'mlops': ['MLflow', 'Kubeflow', 'SageMaker', 'Vertex AI', 'DVC'],
        'deep_learning': ['CNNs', 'RNNs', 'Transformers', 'GANs', 'BERT', 'GPT'],
        'visualization': ['Matplotlib', 'Seaborn', 'Plotly', 'Tableau', 'Power BI'],
        'statistics': ['A/B Testing', 'Hypothesis Testing', 'Bayesian Methods', 'Time Series'],
    }
}


# ============================================================================
# ROLE-SPECIFIC ACHIEVEMENT TEMPLATES
# ============================================================================

ACHIEVEMENT_TEMPLATES = {
    'devops_sre': [
        "Architected and deployed **{technology}** infrastructure on **{cloud}**, achieving **{metric}% uptime** and supporting **{scale}+ microservices**",
        "Designed GitOps-based CI/CD pipelines using **{cicd_tool}** and **{gitops_tool}**, reducing deployment time from **{old_time}** to **{new_time}**",
        "Implemented Infrastructure as Code using **{iac_tool}**, managing **{resource_count}+ resources** across **{env_count} environments**",
        "Built comprehensive observability stack with **{monitoring_tools}**, reducing MTTR by **{mttr_reduction}%**",
        "Led security hardening initiatives including **{security_measures}**, achieving **{compliance}** compliance",
        "Automated disaster recovery procedures achieving RPO of **{rpo}** and RTO of **{rto}**",
        "Reduced cloud infrastructure costs by **{cost_reduction}%** through resource optimization and right-sizing",
        "Implemented **{container_tool}** orchestration for **{container_count}+ containers** with auto-scaling capabilities",
        "Designed and deployed multi-region **{service}** architecture with **{latency}ms P99 latency**",
        "Established SRE practices including SLOs, error budgets, and incident management reducing incidents by **{incident_reduction}%**",
    ],
    'software_engineer': [
        "Designed and implemented **{api_type}** APIs serving **{requests}M+ daily requests** with **{uptime}% availability**",
        "Led migration from monolithic to **microservices architecture**, improving deployment frequency by **{improvement}x**",
        "Optimized database queries and implemented **{caching}** caching, reducing API response times by **{reduction}%**",
        "Built real-time **{feature}** system processing **{events}K+ events/second** using **{technology}**",
        "Implemented comprehensive test coverage achieving **{coverage}%+ code coverage** across all services",
        "Developed **{feature_name}** feature increasing user engagement by **{engagement}%** and revenue by **{revenue}%**",
        "Architected **{system}** system handling **{scale}** concurrent users with sub-**{latency}ms** latency",
        "Mentored **{team_size}** junior developers and established code review practices improving code quality by **{quality}%**",
        "Reduced technical debt by **{debt_reduction}%** through systematic refactoring and documentation",
        "Integrated **{third_party}** APIs enabling **{capability}** and generating **{impact}** in business value",
    ],
    'ds_ml': [
        "Developed and deployed production ML models serving **{predictions}M+ predictions daily** with **{uptime}% uptime**",
        "Built end-to-end ML pipelines using **{mlops_tools}**, reducing model deployment time by **{reduction}%**",
        "Implemented **{model_type}** model achieving **{accuracy}% accuracy**, improving **{metric}** by **{improvement}%**",
        "Designed A/B testing framework for ML models, enabling data-driven model selection with **{confidence}% confidence**",
        "Optimized model inference latency from **{old_latency}ms** to **{new_latency}ms** through **{optimization_technique}**",
        "Created **{dashboard_type}** dashboards providing insights to **{stakeholder_count}+ stakeholders**",
        "Developed NLP pipeline processing **{documents}K+ documents daily** with **{accuracy}% extraction accuracy**",
        "Built recommendation system increasing **{metric}** by **{improvement}%** and driving **{revenue}** in revenue",
        "Implemented feature store serving **{features}+ features** to **{models}+ production models**",
        "Led data quality initiatives reducing data pipeline failures by **{reduction}%** and improving model reliability",
    ]
}


# ============================================================================
# ROLE-SPECIFIC SUMMARY TEMPLATES
# ============================================================================

SUMMARY_TEMPLATES = {
    'devops_sre': [
        "Results-driven DevOps/SRE Engineer with {years}+ years of experience designing and implementing scalable cloud infrastructure, CI/CD pipelines, and observability solutions. Expert in {cloud_platforms} and {key_technologies}. Proven track record of achieving {uptime}% uptime SLAs and reducing deployment times by {deployment_improvement}%. Passionate about automation, reliability engineering, and enabling development teams to ship faster with confidence.",
        "Senior Site Reliability Engineer with {years}+ years specializing in building resilient, highly-available systems at scale. Deep expertise in {cloud_platforms}, {container_tech}, and Infrastructure as Code. Successfully managed infrastructure supporting {scale}+ services with {uptime}% availability. Strong advocate for SRE best practices including SLOs, error budgets, and blameless postmortems.",
        "Cloud Infrastructure Engineer with {years}+ years of hands-on experience in {cloud_platforms} and modern DevOps practices. Skilled in {iac_tools} for infrastructure automation and {cicd_tools} for continuous delivery. Track record of reducing operational toil by {toil_reduction}% and improving system reliability through proactive monitoring and automation.",
    ],
    'software_engineer': [
        "Senior Software Engineer with {years}+ years of experience building scalable, high-performance applications. Proficient in full-stack development with expertise in {languages} and {frameworks}. Strong background in system design, API development, and microservices architecture. Committed to writing clean, maintainable code and implementing best practices in software development lifecycle.",
        "Full-Stack Developer with {years}+ years specializing in {frontend_tech} and {backend_tech}. Experienced in designing and implementing RESTful APIs, microservices, and real-time systems. Proven ability to lead technical initiatives, mentor junior developers, and deliver high-quality software on schedule.",
        "Backend Engineer with {years}+ years of experience in distributed systems and cloud-native development. Expert in {languages} with deep knowledge of {databases} and message queues. Track record of building systems handling {scale}+ requests per second with {uptime}% availability.",
    ],
    'ds_ml': [
        "Data Scientist / ML Engineer with {years}+ years of experience developing and deploying machine learning models at scale. Expert in {ml_frameworks} with a strong foundation in statistical analysis and data engineering. Proven ability to translate business requirements into ML solutions, achieving significant improvements in prediction accuracy and operational efficiency.",
        "Machine Learning Engineer with {years}+ years specializing in end-to-end ML pipeline development and MLOps. Proficient in {ml_frameworks} and {mlops_tools}. Experience deploying models serving {predictions}M+ predictions daily with production-grade reliability and monitoring.",
        "Senior Data Scientist with {years}+ years of experience in predictive modeling, NLP, and deep learning. Skilled in {ml_frameworks} and {data_tools}. Track record of delivering ML solutions that drive measurable business impact, including {impact_metric}% improvement in key metrics.",
    ]
}


# ============================================================================
# COVER LETTER CONTENT TEMPLATES
# ============================================================================

COVER_LETTER_TEMPLATES = {
    'devops_sre': {
        'opening': [
            "I am writing to express my strong interest in the {position} position at {company}. With {years}+ years of experience in DevOps and Site Reliability Engineering, I am excited about the opportunity to contribute to your team's mission of building reliable, scalable infrastructure.",
            "As a passionate DevOps/SRE professional with {years}+ years of experience, I was thrilled to discover the {position} opening at {company}. Your commitment to engineering excellence and innovation aligns perfectly with my career goals.",
        ],
        'body': [
            "In my current role, I have successfully architected and deployed cloud infrastructure on {cloud_platforms}, achieving {uptime}% uptime while supporting {scale}+ microservices. I implemented GitOps-based CI/CD pipelines that reduced deployment time by {deployment_improvement}%, and built comprehensive observability solutions using {monitoring_tools}.",
            "My key achievements include:\n• Designed Infrastructure as Code solutions managing {resource_count}+ cloud resources\n• Reduced MTTR by {mttr_reduction}% through improved monitoring and alerting\n• Led security initiatives achieving {compliance} compliance\n• Automated disaster recovery with RPO of {rpo} and RTO of {rto}",
        ],
        'closing': [
            "I am confident that my technical expertise in {key_technologies} combined with my passion for reliability engineering would make me a valuable addition to your team. I look forward to discussing how I can contribute to {company}'s continued success.",
            "I would welcome the opportunity to discuss how my experience in cloud infrastructure, automation, and SRE practices can help {company} achieve its reliability and scalability goals. Thank you for considering my application.",
        ]
    },
    'software_engineer': {
        'opening': [
            "I am excited to apply for the {position} position at {company}. With {years}+ years of software engineering experience and a passion for building scalable, user-centric applications, I am eager to contribute to your innovative team.",
            "As a Senior Software Engineer with {years}+ years of experience in full-stack development, I was immediately drawn to the {position} opportunity at {company}. Your focus on technical excellence and product innovation resonates strongly with my professional values.",
        ],
        'body': [
            "Throughout my career, I have designed and implemented APIs serving {requests}M+ daily requests with {uptime}% availability. I led the migration from monolithic to microservices architecture, improving deployment frequency and system reliability. My expertise spans {languages} and {frameworks}, with a strong focus on clean code and test-driven development.",
            "Key accomplishments include:\n• Built real-time systems processing {events}K+ events per second\n• Achieved {coverage}%+ test coverage across all services\n• Reduced API response times by {reduction}% through optimization\n• Mentored {team_size}+ developers and established code review best practices",
        ],
        'closing': [
            "I am enthusiastic about the opportunity to bring my technical skills and collaborative approach to {company}. I look forward to discussing how I can contribute to your engineering team's success.",
            "I would love to discuss how my experience in {technologies} and my commitment to engineering excellence can help {company} build exceptional products. Thank you for your consideration.",
        ]
    },
    'ds_ml': {
        'opening': [
            "I am writing to express my interest in the {position} position at {company}. With {years}+ years of experience in machine learning and data science, I am excited about the opportunity to apply my skills to solve challenging problems at scale.",
            "As a Machine Learning Engineer with {years}+ years of experience deploying production ML systems, I was thrilled to see the {position} opening at {company}. Your data-driven approach to innovation aligns perfectly with my expertise and career aspirations.",
        ],
        'body': [
            "In my current role, I have developed and deployed ML models serving {predictions}M+ predictions daily with {uptime}% uptime. I built end-to-end ML pipelines using {mlops_tools}, reducing model deployment time by {reduction}%. My expertise includes {ml_frameworks} and production MLOps practices.",
            "Notable achievements include:\n• Implemented models achieving {accuracy}% accuracy on key metrics\n• Optimized inference latency from {old_latency}ms to {new_latency}ms\n• Built recommendation systems driving {revenue} in incremental revenue\n• Established A/B testing frameworks for data-driven model selection",
        ],
        'closing': [
            "I am confident that my expertise in machine learning, combined with my experience in production systems, would enable me to make significant contributions to {company}'s data science initiatives. I look forward to discussing this opportunity.",
            "I would welcome the chance to discuss how my ML engineering skills and passion for data-driven solutions can help {company} achieve its goals. Thank you for considering my application.",
        ]
    }
}


# ============================================================================
# ATS KEYWORD DATABASE
# ============================================================================

ATS_KEYWORDS = {
    'devops_sre': [
        'CI/CD', 'Infrastructure as Code', 'Kubernetes', 'Docker', 'AWS', 'Azure', 'GCP',
        'Terraform', 'Ansible', 'Jenkins', 'GitOps', 'Prometheus', 'Grafana', 'ELK',
        'Site Reliability', 'SRE', 'DevOps', 'Cloud Infrastructure', 'Automation',
        'Monitoring', 'Observability', 'Incident Management', 'On-call', 'SLO', 'SLA',
        'High Availability', 'Disaster Recovery', 'Security', 'Compliance', 'Scalability',
    ],
    'software_engineer': [
        'Software Development', 'Full Stack', 'Backend', 'Frontend', 'API Development',
        'Microservices', 'REST', 'GraphQL', 'Database', 'SQL', 'NoSQL', 'Agile', 'Scrum',
        'Test-Driven Development', 'Code Review', 'System Design', 'Architecture',
        'Performance Optimization', 'Scalability', 'Clean Code', 'SOLID Principles',
        'Version Control', 'Git', 'CI/CD', 'Unit Testing', 'Integration Testing',
    ],
    'ds_ml': [
        'Machine Learning', 'Deep Learning', 'Data Science', 'Python', 'TensorFlow',
        'PyTorch', 'Scikit-learn', 'NLP', 'Computer Vision', 'Neural Networks',
        'Model Deployment', 'MLOps', 'Feature Engineering', 'A/B Testing', 'Statistics',
        'Data Pipeline', 'ETL', 'SQL', 'Big Data', 'Spark', 'Data Visualization',
        'Predictive Modeling', 'Classification', 'Regression', 'Clustering',
    ]
}


# ============================================================================
# CONTENT GENERATION FUNCTIONS
# ============================================================================

class AIContentGenerator:
    """Enterprise-grade AI content generator for resumes and cover letters"""
    
    def __init__(self, role: str = 'software_engineer'):
        self.role = role
        self.skills_db = ROLE_SKILLS.get(role, ROLE_SKILLS['software_engineer'])
        self.achievement_templates = ACHIEVEMENT_TEMPLATES.get(role, [])
        self.summary_templates = SUMMARY_TEMPLATES.get(role, [])
        self.cover_letter_templates = COVER_LETTER_TEMPLATES.get(role, {})
        self.ats_keywords = ATS_KEYWORDS.get(role, [])
    
    def generate_summary(self, years: int = 5, **kwargs) -> str:
        """Generate a role-specific professional summary"""
        template = random.choice(self.summary_templates)
        
        # Default values based on role
        defaults = self._get_role_defaults()
        defaults['years'] = years
        defaults.update(kwargs)
        
        try:
            return template.format(**defaults)
        except KeyError:
            return template
    
    def generate_bullet_points(self, count: int = 5, **kwargs) -> List[str]:
        """Generate role-specific achievement bullet points"""
        templates = random.sample(
            self.achievement_templates, 
            min(count, len(self.achievement_templates))
        )
        
        defaults = self._get_role_defaults()
        defaults.update(kwargs)
        
        bullets = []
        for template in templates:
            try:
                bullet = template.format(**defaults)
                bullets.append(bullet)
            except KeyError:
                bullets.append(template)
        
        return bullets
    
    def generate_skills_list(self, count: int = 12) -> List[str]:
        """Generate a curated list of role-specific skills"""
        all_skills = []
        for category, skills in self.skills_db.items():
            all_skills.extend(skills[:3])  # Top 3 from each category
        
        return all_skills[:count]
    
    def generate_cover_letter_content(self, company: str, position: str, 
                                       years: int = 5, **kwargs) -> Dict[str, str]:
        """Generate complete cover letter content"""
        defaults = self._get_role_defaults()
        defaults.update({
            'company': company,
            'position': position,
            'years': years,
            **kwargs
        })
        
        content = {}
        for section in ['opening', 'body', 'closing']:
            templates = self.cover_letter_templates.get(section, [])
            if templates:
                template = random.choice(templates)
                try:
                    content[section] = template.format(**defaults)
                except KeyError:
                    content[section] = template
        
        return content
    
    def optimize_for_ats(self, text: str) -> Tuple[str, List[str]]:
        """Analyze text for ATS optimization and suggest improvements"""
        found_keywords = []
        missing_keywords = []
        
        text_lower = text.lower()
        for keyword in self.ats_keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        score = len(found_keywords) / len(self.ats_keywords) * 100 if self.ats_keywords else 0
        
        return {
            'score': round(score, 1),
            'found_keywords': found_keywords,
            'missing_keywords': missing_keywords[:10],  # Top 10 suggestions
            'suggestions': self._generate_ats_suggestions(missing_keywords[:5])
        }
    
    def _get_role_defaults(self) -> Dict:
        """Get default placeholder values for the role"""
        if self.role == 'devops_sre':
            return {
                'cloud_platforms': 'AWS, Azure, and GCP',
                'key_technologies': 'Kubernetes, Terraform, and GitOps',
                'container_tech': 'Kubernetes and Docker',
                'iac_tools': 'Terraform and Ansible',
                'cicd_tools': 'GitHub Actions and ArgoCD',
                'monitoring_tools': 'Prometheus, Grafana, and ELK',
                'technology': 'Kubernetes',
                'cloud': 'AWS',
                'metric': '99.9',
                'scale': '200',
                'cicd_tool': 'GitHub Actions',
                'gitops_tool': 'ArgoCD',
                'old_time': '2 hours',
                'new_time': '15 minutes',
                'iac_tool': 'Terraform',
                'resource_count': '200',
                'env_count': '5',
                'mttr_reduction': '60',
                'security_measures': 'IAM policies, WAF rules, and secrets management',
                'compliance': 'SOC2',
                'rpo': '1 hour',
                'rto': '30 minutes',
                'cost_reduction': '35',
                'container_tool': 'Kubernetes',
                'container_count': '500',
                'service': 'API gateway',
                'latency': '50',
                'incident_reduction': '40',
                'uptime': '99.9',
                'deployment_improvement': '70',
                'toil_reduction': '50',
            }
        elif self.role == 'software_engineer':
            return {
                'languages': 'Python, JavaScript, and Go',
                'frameworks': 'React, Django, and Node.js',
                'frontend_tech': 'React and TypeScript',
                'backend_tech': 'Django and FastAPI',
                'databases': 'PostgreSQL and Redis',
                'api_type': 'RESTful',
                'requests': '10',
                'uptime': '99.9',
                'improvement': '5',
                'caching': 'Redis',
                'reduction': '40',
                'feature': 'notification',
                'events': '100',
                'technology': 'Kafka',
                'coverage': '85',
                'feature_name': 'real-time collaboration',
                'engagement': '25',
                'revenue': '15',
                'system': 'payment processing',
                'scale': '10,000',
                'team_size': '5',
                'quality': '30',
                'debt_reduction': '40',
                'third_party': 'payment gateway',
                'capability': 'seamless transactions',
                'impact': '$2M',
                'technologies': 'Python, React, and cloud services',
            }
        else:  # ds_ml
            return {
                'ml_frameworks': 'TensorFlow, PyTorch, and Scikit-learn',
                'mlops_tools': 'MLflow and Kubeflow',
                'data_tools': 'Pandas, Spark, and Airflow',
                'predictions': '5',
                'uptime': '99.5',
                'reduction': '70',
                'model_type': 'gradient boosting',
                'accuracy': '94',
                'metric': 'conversion rate',
                'confidence': '95',
                'old_latency': '200',
                'new_latency': '50',
                'optimization_technique': 'model quantization',
                'dashboard_type': 'executive',
                'stakeholder_count': '50',
                'documents': '100',
                'features': '500',
                'models': '20',
                'impact_metric': '25',
            }
    
    def _generate_ats_suggestions(self, missing_keywords: List[str]) -> List[str]:
        """Generate suggestions for incorporating missing ATS keywords"""
        suggestions = []
        for keyword in missing_keywords:
            suggestions.append(f"Consider adding '{keyword}' to highlight relevant experience")
        return suggestions


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_role_skills(role: str) -> Dict[str, List[str]]:
    """Get categorized skills for a specific role"""
    return ROLE_SKILLS.get(role, ROLE_SKILLS['software_engineer'])


def get_ats_keywords(role: str) -> List[str]:
    """Get ATS keywords for a specific role"""
    return ATS_KEYWORDS.get(role, ATS_KEYWORDS['software_engineer'])


def generate_content_for_role(role: str, content_type: str, **kwargs) -> str:
    """Convenience function to generate content for a specific role"""
    generator = AIContentGenerator(role)
    
    if content_type == 'summary':
        return generator.generate_summary(**kwargs)
    elif content_type == 'bullets':
        return generator.generate_bullet_points(**kwargs)
    elif content_type == 'skills':
        return generator.generate_skills_list(**kwargs)
    elif content_type == 'cover_letter':
        return generator.generate_cover_letter_content(**kwargs)
    
    return ""
