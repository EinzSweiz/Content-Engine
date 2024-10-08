# Generated by Django 4.2.16 on 2024-09-24 18:31

from django.db import migrations, models
import projects.validator


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_project_added_by_project_added_by_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='handle',
            field=models.SlugField(blank=True, null=True, unique=True, validators=[projects.validator.validate_project_handle]),
        ),
    ]
