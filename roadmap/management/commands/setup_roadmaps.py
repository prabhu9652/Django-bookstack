from django.core.management.base import BaseCommand
from roadmap.models import RoadmapPath, RoadmapPhase, RoadmapSkill, RoadmapHighlight


class Command(BaseCommand):
    help = 'Setup initial roadmap data with enterprise-level content'

    def handle(self, *args, **options):
        self.stdout.write('Setting up roadmap data...')
        
        # Clear existing data
        RoadmapPath.objects.all().delete()
        
        # Create DevOps/SRE Roadmap
        devops_path = self.create_devops_roadmap()
        
        # Create Full-Stack Development Roadmap
        fullstack_path = self.create_fullstack_roadmap()
        
        # Create DSML Roadmap
        dsml_path = self.create_dsml_roadmap()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {RoadmapPath.objects.count()} roadmap paths with '
                f'{RoadmapPhase.objects.count()} phases and '
                f'{RoadmapSkill.objects.count()} skills'
            )
        )

    def create_devops_roadmap(self):
        """Create DevOps/SRE roadmap path"""
        devops_path = RoadmapPath.objects.create(
            name='DevOps / SRE',
            subtitle='Infrastructure, Automation & Reliability Engineering',
            description='Master modern infrastructure automation, cloud platforms, and site reliability engineering practices. Build the foundation for scalable, resilient systems.',
            icon_class='fas fa-cogs',
            difficulty='intermediate',
            estimated_duration='8-12 months',
            order=1
        )
        
        # Add highlights
        highlights = [
            ('Cloud Infrastructure', 'fas fa-cloud'),
            ('Container Orchestration', 'fas fa-cubes'),
            ('CI/CD Automation', 'fas fa-sync-alt'),
            ('Monitoring & Observability', 'fas fa-chart-line'),
        ]
        
        for i, (title, icon) in enumerate(highlights):
            RoadmapHighlight.objects.create(
                roadmap_path=devops_path,
                title=title,
                icon_class=icon,
                order=i
            )
        
        # Foundation Phase
        foundation_phase = RoadmapPhase.objects.create(
            roadmap_path=devops_path,
            name='Foundation & Core Concepts',
            description='Essential infrastructure and automation fundamentals',
            duration='2-3 months',
            order=1
        )
        
        foundation_skills = [
            ('Linux System Administration', 'Command line proficiency, system services, networking basics', True),
            ('Version Control with Git', 'Branching strategies, collaboration workflows, Git best practices', True),
            ('Infrastructure as Code Basics', 'Understanding declarative infrastructure, basic Terraform', True),
            ('Container Fundamentals', 'Docker containers, images, networking, storage', True),
            ('Cloud Platform Basics', 'AWS/Azure/GCP core services, IAM, networking', True),
            ('Scripting & Automation', 'Bash, Python for automation, configuration management', False),
        ]
        
        for i, (name, desc, is_core) in enumerate(foundation_skills):
            RoadmapSkill.objects.create(
                phase=foundation_phase,
                name=name,
                description=desc,
                is_core=is_core,
                order=i
            )
        
        # Intermediate Phase
        intermediate_phase = RoadmapPhase.objects.create(
            roadmap_path=devops_path,
            name='Platform & Orchestration',
            description='Container orchestration and platform engineering',
            duration='3-4 months',
            order=2
        )
        
        intermediate_skills = [
            ('Kubernetes Administration', 'Cluster management, workload deployment, networking, storage', True),
            ('CI/CD Pipeline Design', 'Jenkins, GitLab CI, GitHub Actions, pipeline optimization', True),
            ('Infrastructure Automation', 'Advanced Terraform, Ansible, configuration management', True),
            ('Service Mesh & Networking', 'Istio, Envoy, advanced networking concepts', False),
            ('Security & Compliance', 'Container security, secrets management, policy enforcement', True),
            ('Database Operations', 'Database deployment, backup strategies, performance tuning', False),
        ]
        
        for i, (name, desc, is_core) in enumerate(intermediate_skills):
            RoadmapSkill.objects.create(
                phase=intermediate_phase,
                name=name,
                description=desc,
                is_core=is_core,
                order=i
            )
        
        # Advanced Phase
        advanced_phase = RoadmapPhase.objects.create(
            roadmap_path=devops_path,
            name='Site Reliability & Scale',
            description='Advanced SRE practices and large-scale operations',
            duration='3-5 months',
            order=3
        )
        
        advanced_skills = [
            ('Observability & Monitoring', 'Prometheus, Grafana, distributed tracing, SLI/SLO design', True),
            ('Incident Response & Management', 'On-call practices, post-mortem culture, chaos engineering', True),
            ('Performance Engineering', 'System optimization, capacity planning, load testing', True),
            ('Multi-Cloud & Hybrid', 'Cross-cloud deployments, hybrid architectures, migration strategies', False),
            ('Platform Engineering', 'Internal developer platforms, self-service infrastructure', True),
            ('Cost Optimization', 'Cloud cost management, resource optimization, FinOps practices', False),
        ]
        
        for i, (name, desc, is_core) in enumerate(advanced_skills):
            RoadmapSkill.objects.create(
                phase=advanced_phase,
                name=name,
                description=desc,
                is_core=is_core,
                order=i
            )
        
        return devops_path

    def create_fullstack_roadmap(self):
        """Create Full-Stack Development roadmap path"""
        fullstack_path = RoadmapPath.objects.create(
            name='Full-Stack Development',
            subtitle='Modern Web Applications & Platform Development',
            description='Build end-to-end applications with modern frameworks, APIs, and cloud-native architectures. Master both frontend and backend development.',
            icon_class='fas fa-code',
            difficulty='intermediate',
            estimated_duration='10-14 months',
            order=2
        )
        
        # Add highlights
        highlights = [
            ('Modern Frontend Frameworks', 'fab fa-react'),
            ('Backend APIs & Services', 'fas fa-server'),
            ('Database Design', 'fas fa-database'),
            ('Cloud-Native Development', 'fas fa-cloud-upload-alt'),
        ]
        
        for i, (title, icon) in enumerate(highlights):
            RoadmapHighlight.objects.create(
                roadmap_path=fullstack_path,
                title=title,
                icon_class=icon,
                order=i
            )
        
        # Frontend Foundation Phase
        frontend_phase = RoadmapPhase.objects.create(
            roadmap_path=fullstack_path,
            name='Frontend Development',
            description='Modern frontend development with React and ecosystem',
            duration='3-4 months',
            order=1
        )
        
        frontend_skills = [
            ('JavaScript ES6+ & TypeScript', 'Modern JavaScript features, TypeScript for type safety', True),
            ('React & Component Architecture', 'React hooks, state management, component design patterns', True),
            ('Frontend Build Tools', 'Webpack, Vite, module bundlers, development workflows', True),
            ('State Management', 'Redux, Zustand, context patterns, data flow architecture', True),
            ('CSS & Styling Solutions', 'CSS-in-JS, Tailwind CSS, responsive design, animations', False),
            ('Testing Frontend Applications', 'Jest, React Testing Library, E2E testing with Playwright', False),
        ]
        
        for i, (name, desc, is_core) in enumerate(frontend_skills):
            RoadmapSkill.objects.create(
                phase=frontend_phase,
                name=name,
                description=desc,
                is_core=is_core,
                order=i
            )
        
        # Backend Development Phase
        backend_phase = RoadmapPhase.objects.create(
            roadmap_path=fullstack_path,
            name='Backend Development',
            description='Server-side development with Node.js and Python',
            duration='4-5 months',
            order=2
        )
        
        backend_skills = [
            ('Node.js & Express Framework', 'Server-side JavaScript, REST API development, middleware', True),
            ('Python & Django/FastAPI', 'Python web frameworks, ORM patterns, API development', True),
            ('Database Design & Management', 'PostgreSQL, MongoDB, database optimization, migrations', True),
            ('Authentication & Authorization', 'JWT, OAuth, session management, security best practices', True),
            ('API Design & Documentation', 'RESTful APIs, GraphQL, OpenAPI specification, API versioning', True),
            ('Caching & Performance', 'Redis, application caching, query optimization, CDN integration', False),
        ]
        
        for i, (name, desc, is_core) in enumerate(backend_skills):
            RoadmapSkill.objects.create(
                phase=backend_phase,
                name=name,
                description=desc,
                is_core=is_core,
                order=i
            )
        
        # Full-Stack Integration Phase
        integration_phase = RoadmapPhase.objects.create(
            roadmap_path=fullstack_path,
            name='Full-Stack Integration',
            description='Connecting frontend and backend with modern deployment practices',
            duration='3-5 months',
            order=3
        )
        
        integration_skills = [
            ('Real-time Applications', 'WebSockets, Server-Sent Events, real-time data synchronization', True),
            ('Cloud Deployment & DevOps', 'Docker, Kubernetes, CI/CD for applications, cloud platforms', True),
            ('Microservices Architecture', 'Service decomposition, API gateways, inter-service communication', False),
            ('Performance Optimization', 'Application profiling, bundle optimization, database tuning', True),
            ('Security Implementation', 'HTTPS, CORS, input validation, security headers, vulnerability scanning', True),
            ('Monitoring & Analytics', 'Application monitoring, error tracking, user analytics, logging', False),
        ]
        
        for i, (name, desc, is_core) in enumerate(integration_skills):
            RoadmapSkill.objects.create(
                phase=integration_phase,
                name=name,
                description=desc,
                is_core=is_core,
                order=i
            )
        
        return fullstack_path

    def create_dsml_roadmap(self):
        """Create Data Science & Machine Learning roadmap path"""
        dsml_path = RoadmapPath.objects.create(
            name='Data Science & Machine Learning',
            subtitle='AI/ML Engineering & Data-Driven Systems',
            description='Master data science, machine learning, and AI engineering. Build intelligent systems that learn from data and drive business decisions.',
            icon_class='fas fa-chart-line',
            difficulty='advanced',
            estimated_duration='12-18 months',
            order=3
        )
        
        # Add highlights
        highlights = [
            ('Machine Learning Models', 'fas fa-brain'),
            ('Data Engineering Pipelines', 'fas fa-stream'),
            ('MLOps & Model Deployment', 'fas fa-rocket'),
            ('AI System Architecture', 'fas fa-network-wired'),
        ]
        
        for i, (title, icon) in enumerate(highlights):
            RoadmapHighlight.objects.create(
                roadmap_path=dsml_path,
                title=title,
                icon_class=icon,
                order=i
            )
        
        # Data Foundation Phase
        data_foundation_phase = RoadmapPhase.objects.create(
            roadmap_path=dsml_path,
            name='Data Science Foundation',
            description='Statistical analysis, data manipulation, and exploratory data analysis',
            duration='3-4 months',
            order=1
        )
        
        data_foundation_skills = [
            ('Python for Data Science', 'NumPy, Pandas, data manipulation, statistical computing', True),
            ('Statistical Analysis & Probability', 'Descriptive statistics, hypothesis testing, probability distributions', True),
            ('Data Visualization', 'Matplotlib, Seaborn, Plotly, interactive dashboards', True),
            ('SQL & Database Analytics', 'Advanced SQL, window functions, database optimization for analytics', True),
            ('Exploratory Data Analysis', 'Data profiling, pattern recognition, feature discovery', True),
            ('R Programming', 'R for statistical analysis, ggplot2, statistical modeling', False),
        ]
        
        for i, (name, desc, is_core) in enumerate(data_foundation_skills):
            RoadmapSkill.objects.create(
                phase=data_foundation_phase,
                name=name,
                description=desc,
                is_core=is_core,
                order=i
            )
        
        # Machine Learning Phase
        ml_phase = RoadmapPhase.objects.create(
            roadmap_path=dsml_path,
            name='Machine Learning Engineering',
            description='ML algorithms, model development, and evaluation techniques',
            duration='4-6 months',
            order=2
        )
        
        ml_skills = [
            ('Supervised Learning Algorithms', 'Linear/logistic regression, decision trees, ensemble methods', True),
            ('Unsupervised Learning', 'Clustering, dimensionality reduction, anomaly detection', True),
            ('Deep Learning & Neural Networks', 'TensorFlow, PyTorch, CNN, RNN, transformer architectures', True),
            ('Feature Engineering', 'Feature selection, transformation, encoding, scaling techniques', True),
            ('Model Evaluation & Validation', 'Cross-validation, metrics, bias-variance tradeoff, A/B testing', True),
            ('Natural Language Processing', 'Text processing, sentiment analysis, language models, embeddings', False),
        ]
        
        for i, (name, desc, is_core) in enumerate(ml_skills):
            RoadmapSkill.objects.create(
                phase=ml_phase,
                name=name,
                description=desc,
                is_core=is_core,
                order=i
            )
        
        # MLOps & Production Phase
        mlops_phase = RoadmapPhase.objects.create(
            roadmap_path=dsml_path,
            name='MLOps & Production Systems',
            description='Deploying, monitoring, and scaling ML systems in production',
            duration='5-8 months',
            order=3
        )
        
        mlops_skills = [
            ('ML Pipeline Development', 'Airflow, Kubeflow, MLflow, experiment tracking, versioning', True),
            ('Model Deployment & Serving', 'REST APIs, model serving frameworks, containerization, scaling', True),
            ('Data Engineering for ML', 'ETL pipelines, data lakes, streaming data, feature stores', True),
            ('ML Monitoring & Observability', 'Model drift detection, performance monitoring, data quality', True),
            ('Cloud ML Platforms', 'AWS SageMaker, Google AI Platform, Azure ML, serverless ML', True),
            ('Edge ML & Optimization', 'Model compression, quantization, edge deployment, mobile ML', False),
        ]
        
        for i, (name, desc, is_core) in enumerate(mlops_skills):
            RoadmapSkill.objects.create(
                phase=mlops_phase,
                name=name,
                description=desc,
                is_core=is_core,
                order=i
            )
        
        return dsml_path