"""
Management command to update the DSML roadmap with comprehensive curriculum
Based on industry-standard Data Science & Machine Learning curriculum structure
"""
from django.core.management.base import BaseCommand
from roadmap.models import RoadmapPath, RoadmapPhase, RoadmapSkill, RoadmapHighlight


class Command(BaseCommand):
    help = 'Update DSML roadmap with comprehensive curriculum'

    def handle(self, *args, **options):
        self.stdout.write('Updating DSML Roadmap...')
        
        # Get or create the DSML path
        dsml_path, created = RoadmapPath.objects.get_or_create(
            slug='data-science-machine-learning',
            defaults={
                'name': 'Data Science & Machine Learning',
                'subtitle': 'From Data Analysis to Production ML Systems',
                'description': 'A comprehensive learning path covering data analysis, statistics, machine learning, deep learning, and MLOps. Master the skills needed to become a Data Scientist or ML Engineer.',
                'icon_class': 'fas fa-brain',
                'difficulty': 'intermediate',
                'estimated_duration': '12-18 months',
                'order': 3,
                'is_active': True,
            }
        )
        
        if not created:
            dsml_path.name = 'Data Science & Machine Learning'
            dsml_path.subtitle = 'From Data Analysis to Production ML Systems'
            dsml_path.description = 'A comprehensive learning path covering data analysis, statistics, machine learning, deep learning, and MLOps. Master the skills needed to become a Data Scientist or ML Engineer.'
            dsml_path.icon_class = 'fas fa-brain'
            dsml_path.difficulty = 'intermediate'
            dsml_path.estimated_duration = '12-18 months'
            dsml_path.save()
        
        # Delete existing phases and skills for clean update
        dsml_path.phases.all().delete()
        dsml_path.highlights.all().delete()
        
        # Create highlights
        highlights = [
            ('Python & SQL Mastery', 'fab fa-python', 1),
            ('Statistics & Probability', 'fas fa-chart-bar', 2),
            ('Machine Learning Algorithms', 'fas fa-robot', 3),
            ('Deep Learning & Neural Networks', 'fas fa-network-wired', 4),
            ('MLOps & Deployment', 'fas fa-cloud-upload-alt', 5),
            ('Real-World Projects', 'fas fa-project-diagram', 6),
        ]
        
        for title, icon, order in highlights:
            RoadmapHighlight.objects.create(
                roadmap_path=dsml_path,
                title=title,
                icon_class=icon,
                order=order
            )
        
        # Phase 1: Beginner Module - The Basics
        phase1 = RoadmapPhase.objects.create(
            roadmap_path=dsml_path,
            name='Beginner Module: The Basics',
            description='Build a strong foundation with essential tools and programming skills for data science.',
            duration='16-20 weeks',
            order=1,
            is_active=True
        )
        
        phase1_skills = [
            ('SQL Fundamentals', 'DDL, DML, DCL, TCL commands. SELECT, INSERT, UPDATE, DELETE operations. WHERE, GROUP BY, HAVING, ORDER BY clauses.', True, 1),
            ('SQL Advanced Queries', 'JOINs (INNER, LEFT, RIGHT, FULL, CROSS, SELF). Subqueries, Correlated Subqueries, CTEs. Aggregate and Scalar Functions.', True, 2),
            ('SQL Database Objects', 'Views, Stored Procedures, Triggers, Functions. Primary Keys, Foreign Keys, Constraints. Indexes and Query Optimization.', True, 3),
            ('Excel for Data Analysis', 'Data manipulation, Pivot Tables, VLOOKUP/HLOOKUP. Statistical functions, Charts and Visualizations. Data cleaning and transformation.', True, 4),
            ('Python Programming Basics', 'Variables, Data Types, Operators. Control Flow (if/else, loops). Functions, Modules, and Packages.', True, 5),
            ('Python Data Structures', 'Lists, Tuples, Dictionaries, Sets. List comprehensions, Generators. File handling and I/O operations.', True, 6),
            ('Python for Data Science', 'NumPy arrays and operations. Pandas DataFrames and Series. Data manipulation and cleaning.', True, 7),
            ('Tableau Fundamentals', 'Connecting to data sources. Building visualizations and dashboards. Calculated fields and parameters.', True, 8),
        ]
        
        for name, desc, is_core, order in phase1_skills:
            RoadmapSkill.objects.create(
                phase=phase1,
                name=name,
                description=desc,
                is_core=is_core,
                order=order
            )
        
        # Phase 2: Intermediate Module - Data Analysis & Visualization
        phase2 = RoadmapPhase.objects.create(
            roadmap_path=dsml_path,
            name='Intermediate Module: Data Analysis & Visualization',
            description='Master data analysis techniques, statistics, and visualization for insights.',
            duration='12-16 weeks',
            order=2,
            is_active=True
        )
        
        phase2_skills = [
            ('Exploratory Data Analysis (EDA)', 'Data profiling and summary statistics. Identifying patterns, outliers, and anomalies. Data quality assessment.', True, 1),
            ('Data Visualization with Python', 'Matplotlib for static visualizations. Seaborn for statistical graphics. Plotly for interactive charts.', True, 2),
            ('Probability Theory', 'Probability distributions (Normal, Binomial, Poisson). Conditional probability and Bayes theorem. Random variables and expectations.', True, 3),
            ('Descriptive Statistics', 'Measures of central tendency (mean, median, mode). Measures of dispersion (variance, std dev). Percentiles and quartiles.', True, 4),
            ('Inferential Statistics', 'Hypothesis testing (t-tests, chi-square, ANOVA). Confidence intervals. P-values and statistical significance.', True, 5),
            ('Regression Analysis', 'Simple and Multiple Linear Regression. Assumptions and diagnostics. Interpretation of coefficients.', True, 6),
            ('A/B Testing & Experimentation', 'Designing experiments. Sample size calculation. Analyzing experiment results.', True, 7),
            ('Product Analytics', 'User behavior analysis. Funnel analysis and conversion metrics. Cohort analysis and retention.', False, 8),
        ]
        
        for name, desc, is_core, order in phase2_skills:
            RoadmapSkill.objects.create(
                phase=phase2,
                name=name,
                description=desc,
                is_core=is_core,
                order=order
            )
        
        # Phase 3: Domain Analytics (Elective)
        phase3 = RoadmapPhase.objects.create(
            roadmap_path=dsml_path,
            name='Special Elective: Domain Analytics',
            description='Apply data science skills to specific industry domains.',
            duration='6-8 weeks',
            order=3,
            is_active=True
        )
        
        phase3_skills = [
            ('E-commerce Analytics', 'Customer segmentation. Recommendation systems basics. Sales forecasting and inventory optimization.', False, 1),
            ('Healthcare Analytics', 'Patient outcome prediction. Clinical data analysis. Healthcare metrics and KPIs.', False, 2),
            ('Financial Analytics', 'Risk assessment and credit scoring. Fraud detection fundamentals. Time series for financial data.', False, 3),
            ('Marketing Analytics', 'Customer lifetime value (CLV). Attribution modeling. Campaign performance analysis.', False, 4),
        ]
        
        for name, desc, is_core, order in phase3_skills:
            RoadmapSkill.objects.create(
                phase=phase3,
                name=name,
                description=desc,
                is_core=is_core,
                order=order
            )
        
        # Phase 4: Advanced Module - Machine Learning
        phase4 = RoadmapPhase.objects.create(
            roadmap_path=dsml_path,
            name='Advanced Module: Machine Learning',
            description='Master machine learning algorithms, model building, and evaluation techniques.',
            duration='20-24 weeks',
            order=4,
            is_active=True
        )
        
        phase4_skills = [
            ('Mathematics for ML', 'Linear Algebra (vectors, matrices, eigenvalues). Calculus (derivatives, gradients, optimization). Probability distributions for ML.', True, 1),
            ('Supervised Learning: Regression', 'Linear Regression, Ridge, Lasso. Polynomial Regression. Regularization techniques.', True, 2),
            ('Supervised Learning: Classification', 'Logistic Regression. Decision Trees and Random Forests. Support Vector Machines (SVM).', True, 3),
            ('Ensemble Methods', 'Bagging and Boosting. XGBoost, LightGBM, CatBoost. Model stacking and blending.', True, 4),
            ('Unsupervised Learning', 'K-Means and Hierarchical Clustering. DBSCAN and density-based methods. Dimensionality Reduction (PCA, t-SNE, UMAP).', True, 5),
            ('Model Evaluation & Validation', 'Cross-validation techniques. Metrics (Accuracy, Precision, Recall, F1, AUC-ROC). Bias-Variance tradeoff.', True, 6),
            ('Feature Engineering', 'Feature selection methods. Feature transformation and scaling. Handling categorical variables.', True, 7),
            ('Hyperparameter Tuning', 'Grid Search and Random Search. Bayesian Optimization. AutoML concepts.', True, 8),
            ('Time Series Analysis', 'ARIMA and SARIMA models. Exponential Smoothing. Prophet for forecasting.', True, 9),
            ('Natural Language Processing', 'Text preprocessing and tokenization. TF-IDF and Word Embeddings. Sentiment Analysis and Text Classification.', True, 10),
        ]
        
        for name, desc, is_core, order in phase4_skills:
            RoadmapSkill.objects.create(
                phase=phase4,
                name=name,
                description=desc,
                is_core=is_core,
                order=order
            )
        
        # Phase 5: Deep Learning
        phase5 = RoadmapPhase.objects.create(
            roadmap_path=dsml_path,
            name='Advanced Module: Deep Learning',
            description='Master neural networks, deep learning architectures, and advanced AI techniques.',
            duration='12-16 weeks',
            order=5,
            is_active=True
        )
        
        phase5_skills = [
            ('Neural Network Fundamentals', 'Perceptrons and activation functions. Backpropagation algorithm. Loss functions and optimizers.', True, 1),
            ('Deep Learning Frameworks', 'TensorFlow and Keras. PyTorch fundamentals. Model building and training.', True, 2),
            ('Convolutional Neural Networks (CNNs)', 'Image classification. Object detection. Transfer learning with pretrained models.', True, 3),
            ('Recurrent Neural Networks (RNNs)', 'Sequence modeling. LSTM and GRU architectures. Text generation and language models.', True, 4),
            ('Transformers & Attention', 'Attention mechanisms. Transformer architecture. BERT, GPT, and modern LLMs.', True, 5),
            ('Autoencoders & GANs', 'Variational Autoencoders (VAE). Generative Adversarial Networks. Image generation and style transfer.', False, 6),
            ('Computer Vision Applications', 'Image segmentation. Face recognition. Video analysis.', False, 7),
            ('Advanced NLP with Deep Learning', 'Named Entity Recognition. Question Answering. Text summarization.', False, 8),
        ]
        
        for name, desc, is_core, order in phase5_skills:
            RoadmapSkill.objects.create(
                phase=phase5,
                name=name,
                description=desc,
                is_core=is_core,
                order=order
            )
        
        # Phase 6: Generative AI (Elective)
        phase6 = RoadmapPhase.objects.create(
            roadmap_path=dsml_path,
            name='Special Elective: Generative AI',
            description='Explore cutting-edge generative AI technologies and applications.',
            duration='6-8 weeks',
            order=6,
            is_active=True
        )
        
        phase6_skills = [
            ('Large Language Models (LLMs)', 'Understanding GPT architecture. Prompt engineering techniques. Fine-tuning LLMs.', True, 1),
            ('LangChain & RAG', 'Building LLM applications. Retrieval Augmented Generation. Vector databases and embeddings.', True, 2),
            ('Diffusion Models', 'Image generation with Stable Diffusion. Text-to-image pipelines. Model customization.', False, 3),
            ('AI Agents & Automation', 'Building autonomous agents. Tool use and function calling. Multi-agent systems.', False, 4),
        ]
        
        for name, desc, is_core, order in phase6_skills:
            RoadmapSkill.objects.create(
                phase=phase6,
                name=name,
                description=desc,
                is_core=is_core,
                order=order
            )
        
        # Phase 7: MLOps & Production
        phase7 = RoadmapPhase.objects.create(
            roadmap_path=dsml_path,
            name='MLOps & Production Systems',
            description='Learn to deploy, monitor, and maintain ML models in production environments.',
            duration='8-12 weeks',
            order=7,
            is_active=True
        )
        
        phase7_skills = [
            ('ML Pipeline Development', 'Data pipelines with Airflow/Prefect. Feature stores. Experiment tracking with MLflow.', True, 1),
            ('Model Deployment', 'REST APIs with Flask/FastAPI. Model serialization (pickle, ONNX). Containerization with Docker.', True, 2),
            ('Cloud ML Platforms', 'AWS SageMaker. Google Cloud AI Platform. Azure Machine Learning.', True, 3),
            ('Model Monitoring', 'Data drift detection. Model performance monitoring. A/B testing in production.', True, 4),
            ('ML System Design', 'Designing scalable ML systems. Batch vs real-time inference. Cost optimization.', True, 5),
            ('Data Engineering for ML', 'ETL pipelines. Data warehousing concepts. Spark for big data processing.', False, 6),
        ]
        
        for name, desc, is_core, order in phase7_skills:
            RoadmapSkill.objects.create(
                phase=phase7,
                name=name,
                description=desc,
                is_core=is_core,
                order=order
            )
        
        # Phase 8: Projects & Case Studies
        phase8 = RoadmapPhase.objects.create(
            roadmap_path=dsml_path,
            name='Projects & Case Studies',
            description='Apply your skills to real-world projects and build a strong portfolio.',
            duration='Ongoing',
            order=8,
            is_active=True
        )
        
        phase8_skills = [
            ('End-to-End ML Project', 'Problem definition to deployment. Data collection and preprocessing. Model selection and optimization.', True, 1),
            ('Kaggle Competitions', 'Participating in data science competitions. Learning from top solutions. Building competitive models.', False, 2),
            ('Industry Case Studies', 'E-commerce recommendation systems. Fraud detection systems. Demand forecasting.', True, 3),
            ('Portfolio Development', 'GitHub project showcase. Technical blog writing. Presenting ML projects.', True, 4),
        ]
        
        for name, desc, is_core, order in phase8_skills:
            RoadmapSkill.objects.create(
                phase=phase8,
                name=name,
                description=desc,
                is_core=is_core,
                order=order
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully updated DSML roadmap with comprehensive curriculum!'))
        
        # Print summary
        total_phases = dsml_path.phases.count()
        total_skills = RoadmapSkill.objects.filter(phase__roadmap_path=dsml_path).count()
        self.stdout.write(f'Total Phases: {total_phases}')
        self.stdout.write(f'Total Skills: {total_skills}')
