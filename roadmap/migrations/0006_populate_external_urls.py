# Generated migration to populate external URLs for journey tools

from django.db import migrations

# Tool name to official documentation URL mapping
TOOL_URLS = {
    # DevOps / SRE Tools
    'AWS': 'https://docs.aws.amazon.com/',
    'Azure': 'https://learn.microsoft.com/en-us/azure/',
    'GCP': 'https://cloud.google.com/docs',
    'DigitalOcean': 'https://docs.digitalocean.com/',
    'AWS Migration': 'https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-guide/',
    'Terraform': 'https://developer.hashicorp.com/terraform/docs',
    'Terragrunt': 'https://terragrunt.gruntwork.io/docs/',
    'Shell scripting': 'https://www.gnu.org/software/bash/manual/',
    'Docker': 'https://docs.docker.com/',
    'Kubernetes': 'https://kubernetes.io/docs/',
    'K8s': 'https://kubernetes.io/docs/',
    'EKS': 'https://docs.aws.amazon.com/eks/',
    'AKS': 'https://learn.microsoft.com/en-us/azure/aks/',
    'GKE': 'https://cloud.google.com/kubernetes-engine/docs',
    'Jenkins': 'https://www.jenkins.io/doc/',
    'Ansible': 'https://docs.ansible.com/',
    'Puppet': 'https://www.puppet.com/docs',
    'Packer': 'https://developer.hashicorp.com/packer/docs',
    'Python': 'https://docs.python.org/3/',
    'GIT': 'https://git-scm.com/doc',
    'Git': 'https://git-scm.com/doc',
    'Github': 'https://docs.github.com/',
    'GitHub': 'https://docs.github.com/',
    'Bitbucket': 'https://support.atlassian.com/bitbucket-cloud/',
    'GitLab': 'https://docs.gitlab.com/',
    'Bamboo': 'https://confluence.atlassian.com/bamboo/',
    'GitLab CI/CD': 'https://docs.gitlab.com/ee/ci/',
    'GitHub Actions': 'https://docs.github.com/en/actions',
    
    # Full-Stack Development Tools
    'JavaScript': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
    'TypeScript': 'https://www.typescriptlang.org/docs/',
    'Java': 'https://docs.oracle.com/en/java/',
    'Go': 'https://go.dev/doc/',
    'React': 'https://react.dev/learn',
    'Vue.js': 'https://vuejs.org/guide/',
    'Node.js': 'https://nodejs.org/docs/',
    'Django': 'https://docs.djangoproject.com/',
    'FastAPI': 'https://fastapi.tiangolo.com/',
    'PostgreSQL': 'https://www.postgresql.org/docs/',
    'MySQL': 'https://dev.mysql.com/doc/',
    'MongoDB': 'https://www.mongodb.com/docs/',
    'Redis': 'https://redis.io/docs/',
    'REST APIs': 'https://restfulapi.net/',
    'GraphQL': 'https://graphql.org/learn/',
    'CI/CD': 'https://docs.github.com/en/actions',
    'System Design': 'https://github.com/donnemartin/system-design-primer',
    
    # Data Science & Machine Learning Tools
    'R': 'https://www.r-project.org/other-docs.html',
    'SQL': 'https://www.w3schools.com/sql/',
    'Scala': 'https://docs.scala-lang.org/',
    'TensorFlow': 'https://www.tensorflow.org/learn',
    'PyTorch': 'https://pytorch.org/docs/',
    'Scikit-learn': 'https://scikit-learn.org/stable/documentation.html',
    'Keras': 'https://keras.io/guides/',
    'Pandas': 'https://pandas.pydata.org/docs/',
    'NumPy': 'https://numpy.org/doc/',
    'Spark': 'https://spark.apache.org/docs/latest/',
    'Airflow': 'https://airflow.apache.org/docs/',
    'AWS SageMaker': 'https://docs.aws.amazon.com/sagemaker/',
    'MLflow': 'https://mlflow.org/docs/latest/',
    'Matplotlib': 'https://matplotlib.org/stable/contents.html',
    'Seaborn': 'https://seaborn.pydata.org/',
    'Tableau': 'https://help.tableau.com/',
    'BigQuery': 'https://cloud.google.com/bigquery/docs',
}


def populate_external_urls(apps, schema_editor):
    JourneySkill = apps.get_model('roadmap', 'JourneySkill')
    
    for skill in JourneySkill.objects.all():
        if skill.name in TOOL_URLS:
            skill.external_url = TOOL_URLS[skill.name]
            skill.save()


def reverse_populate(apps, schema_editor):
    JourneySkill = apps.get_model('roadmap', 'JourneySkill')
    JourneySkill.objects.all().update(external_url='')


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0005_add_external_url_to_journey_skill'),
    ]

    operations = [
        migrations.RunPython(populate_external_urls, reverse_populate),
    ]
