from django.db import migrations
from django.contrib.sites.models import Site

def create_default_site(apps, schema_editor):
    Site.objects.all().delete()
    Site.objects.create(
        id=1,
        domain='127.0.0.1:8000',
        name='localhost'
    )

class Migration(migrations.Migration):
    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(create_default_site),
    ] 