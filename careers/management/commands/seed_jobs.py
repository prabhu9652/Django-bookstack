"""
Management command to seed production-ready job postings.
These job postings are designed to match real industry standards.
"""
from django.core.management.base import BaseCommand
from careers.models import JobPosting


class Command(BaseCommand):
    help = 'Seeds the database with industry-grade job postings'

    def handle(self, *args, **options):
        jobs_data = [
            # ============================================
            # DevOps Engineer
            # ============================================
            {
                'title': 'DevOps Engineer',
                'department': 'Platform Engineering',
                'location': 'San Francisco, CA',
                'location_type': 'hybrid',
                'employment_type': 'full_time',
                'experience_range': '3-5 years',
                'salary_range': '$140,000 - $180,000',
                'description': '''We're looking for a DevOps Engineer to join our Platform Engineering team and help us build and maintain the infrastructure that powers our products.

You'll work closely with development teams to design, implement, and optimize our CI/CD pipelines, cloud infrastructure, and monitoring systems. This role is critical to ensuring our services are reliable, scalable, and secure.

This is a high-impact position where you'll have the autonomy to make architectural decisions and implement best practices that affect the entire engineering organization.''',
                'responsibilities': '''Design, build, and maintain CI/CD pipelines for multiple services and applications
Manage and optimize cloud infrastructure on AWS (EC2, EKS, RDS, S3, Lambda)
Implement Infrastructure as Code using Terraform and CloudFormation
Set up and maintain monitoring, alerting, and logging systems (Prometheus, Grafana, ELK)
Automate operational tasks and reduce manual intervention through scripting
Collaborate with development teams to improve deployment processes and reduce release cycles
Implement security best practices and ensure compliance with SOC 2 requirements
Participate in on-call rotation and incident response
Document infrastructure architecture and operational procedures
Mentor junior engineers and contribute to team knowledge sharing''',
                'requirements': '''3+ years of experience in DevOps, SRE, or Platform Engineering roles
Strong proficiency with Linux systems administration and Bash scripting
Hands-on experience with containerization (Docker) and orchestration (Kubernetes)
Experience with Infrastructure as Code tools (Terraform, CloudFormation, or Pulumi)
Proficiency with CI/CD tools (GitHub Actions, GitLab CI, Jenkins, or CircleCI)
Experience with monitoring and observability tools (Prometheus, Grafana, Datadog)
Solid understanding of networking concepts (TCP/IP, DNS, load balancing, firewalls)
Experience with at least one major cloud provider (AWS preferred)
Strong troubleshooting and problem-solving skills
Excellent communication skills and ability to work cross-functionally''',
                'nice_to_have': '''Experience with service mesh technologies (Istio, Linkerd)
Knowledge of GitOps practices and tools (ArgoCD, Flux)
Experience with secrets management (HashiCorp Vault, AWS Secrets Manager)
Familiarity with compliance frameworks (SOC 2, HIPAA, PCI-DSS)
Experience with cost optimization and FinOps practices
Contributions to open-source DevOps tools
AWS or Kubernetes certifications''',
                'benefits': '''Competitive salary with equity compensation
Flexible hybrid work arrangement (3 days in office)
Comprehensive health, dental, and vision insurance
401(k) with 4% company match
$2,500 annual learning and development budget
Home office setup stipend
Unlimited PTO with minimum 3 weeks encouraged
Parental leave (16 weeks paid)
Monthly wellness stipend
Regular team offsites and engineering summits''',
                'tech_stack': ['AWS', 'Kubernetes', 'Docker', 'Terraform', 'GitHub Actions', 'Prometheus', 'Grafana', 'Python', 'Bash', 'PostgreSQL', 'Redis', 'Elasticsearch'],
            },
            # ============================================
            # MLOps Engineer
            # ============================================
            {
                'title': 'MLOps Engineer',
                'department': 'Machine Learning Platform',
                'location': 'Remote (US)',
                'location_type': 'remote',
                'employment_type': 'full_time',
                'experience_range': '4-6 years',
                'salary_range': '$160,000 - $200,000',
                'description': '''We're seeking an MLOps Engineer to bridge the gap between our data science team and production systems. You'll be responsible for building and maintaining the infrastructure that enables our ML models to run reliably at scale.

In this role, you'll design ML pipelines, implement model versioning and monitoring systems, and ensure our machine learning workloads are efficient and cost-effective. You'll work at the intersection of software engineering, data engineering, and machine learning.

This is an opportunity to shape the future of our ML platform and directly impact how we deliver AI-powered features to millions of users.''',
                'responsibilities': '''Design and implement end-to-end ML pipelines for training, validation, and deployment
Build and maintain model serving infrastructure for real-time and batch inference
Implement model versioning, experiment tracking, and reproducibility systems using MLflow
Create monitoring and alerting systems for model performance and data drift detection
Optimize ML workloads for cost and performance on cloud infrastructure
Collaborate with data scientists to productionize research models
Develop automated testing frameworks for ML models and data pipelines
Manage GPU clusters and optimize resource utilization
Implement feature stores and data versioning systems
Document best practices and create self-service tools for the ML team''',
                'requirements': '''4+ years of experience in MLOps, ML Engineering, or related roles
Strong Python programming skills with experience in production systems
Experience with ML frameworks (TensorFlow, PyTorch, or scikit-learn)
Hands-on experience with MLflow, Kubeflow, or similar ML platforms
Proficiency with containerization (Docker) and orchestration (Kubernetes)
Experience with cloud ML services (AWS SageMaker, GCP AI Platform, or Azure ML)
Understanding of ML model lifecycle: training, validation, deployment, monitoring
Experience with data pipeline tools (Airflow, Prefect, or Dagster)
Strong understanding of software engineering best practices
Excellent problem-solving skills and attention to detail''',
                'nice_to_have': '''Experience with feature stores (Feast, Tecton)
Knowledge of model optimization techniques (quantization, pruning, distillation)
Experience with real-time inference systems and low-latency requirements
Familiarity with A/B testing frameworks for ML models
Experience with LLM deployment and fine-tuning
Knowledge of data governance and ML compliance requirements
Publications or contributions to ML/MLOps open-source projects''',
                'benefits': '''Competitive salary with equity compensation
Fully remote position with flexible hours
Comprehensive health, dental, and vision insurance
401(k) with 4% company match
$3,000 annual learning budget (conferences, courses, certifications)
Latest MacBook Pro and home office equipment
Unlimited PTO with minimum 3 weeks encouraged
Parental leave (16 weeks paid)
Annual company retreat
Access to GPU resources for personal ML projects''',
                'tech_stack': ['Python', 'TensorFlow', 'PyTorch', 'MLflow', 'Kubeflow', 'AWS SageMaker', 'Docker', 'Kubernetes', 'Airflow', 'PostgreSQL', 'Redis', 'Spark'],
            },
            # ============================================
            # Data Science / ML Engineer
            # ============================================
            {
                'title': 'Data Science / Machine Learning Engineer',
                'department': 'Data Science',
                'location': 'New York, NY',
                'location_type': 'hybrid',
                'employment_type': 'full_time',
                'experience_range': '2-4 years',
                'salary_range': '$130,000 - $170,000',
                'description': '''We're looking for a Data Science / Machine Learning Engineer to join our growing team and help us build intelligent features that delight our users.

You'll work on a variety of ML problems including recommendation systems, natural language processing, and predictive analytics. This role combines hands-on model development with the engineering skills needed to deploy models to production.

You'll collaborate closely with product managers, engineers, and designers to identify opportunities where ML can create value, and then build the solutions end-to-end.''',
                'responsibilities': '''Develop and deploy machine learning models for production use cases
Analyze large datasets to extract insights and identify patterns
Build and maintain data pipelines for feature engineering
Collaborate with product teams to define ML-powered features and success metrics
Design and run A/B experiments to measure model impact
Create visualizations and dashboards to communicate findings to stakeholders
Write clean, maintainable code following software engineering best practices
Stay current with ML research and evaluate new techniques for applicability
Document models, experiments, and findings for knowledge sharing
Participate in code reviews and contribute to team technical standards''',
                'requirements': '''2+ years of experience in data science, machine learning, or related roles
Strong proficiency in Python and SQL
Experience with ML libraries (scikit-learn, TensorFlow, PyTorch, or XGBoost)
Solid foundation in statistics and machine learning fundamentals
Experience with data manipulation tools (Pandas, NumPy, Spark)
Proficiency with data visualization (Matplotlib, Seaborn, Plotly, or Tableau)
Experience deploying models to production environments
Strong communication skills and ability to explain technical concepts to non-technical audiences
Bachelor's or Master's degree in Computer Science, Statistics, Mathematics, or related field
Portfolio of ML projects (personal, academic, or professional)''',
                'nice_to_have': '''Experience with deep learning and neural networks
Knowledge of NLP techniques and transformer models
Experience with recommendation systems
Familiarity with cloud platforms (AWS, GCP, or Azure)
Experience with experiment tracking tools (MLflow, Weights & Biases)
Knowledge of causal inference methods
Publications in ML conferences or journals''',
                'benefits': '''Competitive salary with equity compensation
Flexible hybrid work arrangement (2 days in office)
Comprehensive health, dental, and vision insurance
401(k) with 4% company match
$2,000 annual learning and conference budget
Latest MacBook Pro and peripherals
Unlimited PTO with minimum 3 weeks encouraged
Parental leave (16 weeks paid)
Commuter benefits
Weekly team lunches and monthly social events''',
                'tech_stack': ['Python', 'SQL', 'Pandas', 'scikit-learn', 'TensorFlow', 'PyTorch', 'Spark', 'Airflow', 'PostgreSQL', 'Redshift', 'Tableau', 'Git'],
            },
            # ============================================
            # Full-Stack Engineer (DevOps-aware)
            # ============================================
            {
                'title': 'Full-Stack Engineer',
                'department': 'Product Engineering',
                'location': 'Austin, TX',
                'location_type': 'hybrid',
                'employment_type': 'full_time',
                'experience_range': '3-5 years',
                'salary_range': '$135,000 - $175,000',
                'description': '''We're looking for a Full-Stack Engineer with DevOps awareness to join our Product Engineering team. You'll build features end-to-end, from database design to user interface, and take ownership of deploying and maintaining your code in production.

This role is ideal for engineers who enjoy working across the stack and want to understand how their code runs in production. You'll work on user-facing features that directly impact our customers while also contributing to our infrastructure and deployment processes.

We value engineers who can think holistically about systems and take pride in building reliable, scalable software.''',
                'responsibilities': '''Build and maintain full-stack features using React and Django/FastAPI
Design and implement RESTful APIs and database schemas
Write clean, tested, and well-documented code
Deploy and monitor applications in production environments
Collaborate with designers to implement responsive, accessible user interfaces
Participate in architecture discussions and technical planning
Set up and maintain CI/CD pipelines for your team's services
Troubleshoot production issues and implement fixes
Contribute to shared libraries and internal tools
Mentor junior engineers and participate in code reviews''',
                'requirements': '''3+ years of professional software development experience
Strong proficiency in JavaScript/TypeScript and a modern frontend framework (React preferred)
Experience with backend development in Python (Django or FastAPI) or Node.js
Solid understanding of relational databases (PostgreSQL, MySQL)
Experience with RESTful API design and implementation
Familiarity with CI/CD concepts and tools (GitHub Actions, GitLab CI)
Basic understanding of cloud services (AWS, GCP, or Azure)
Experience with containerization (Docker)
Strong problem-solving skills and attention to code quality
Excellent communication and collaboration skills''',
                'nice_to_have': '''Experience with Kubernetes and container orchestration
Knowledge of Infrastructure as Code (Terraform, CloudFormation)
Experience with message queues (RabbitMQ, Kafka, SQS)
Familiarity with monitoring tools (Datadog, New Relic, Prometheus)
Experience with GraphQL
Knowledge of web security best practices (OWASP)
Experience with mobile development (React Native)
Contributions to open-source projects''',
                'benefits': '''Competitive salary with equity compensation
Flexible hybrid work arrangement (2-3 days in office)
Comprehensive health, dental, and vision insurance
401(k) with 4% company match
$2,500 annual learning and development budget
Latest MacBook Pro and home office stipend
Unlimited PTO with minimum 3 weeks encouraged
Parental leave (16 weeks paid)
Free lunch when in office
Quarterly team events and annual company offsite''',
                'tech_stack': ['React', 'TypeScript', 'Python', 'Django', 'FastAPI', 'PostgreSQL', 'Redis', 'Docker', 'AWS', 'GitHub Actions', 'Terraform', 'Datadog'],
            },
        ]

        created_count = 0
        updated_count = 0

        for job_data in jobs_data:
            job, created = JobPosting.objects.update_or_create(
                title=job_data['title'],
                department=job_data['department'],
                defaults=job_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {job.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: {job.title}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {created_count} jobs, updated {updated_count} jobs.'
        ))
