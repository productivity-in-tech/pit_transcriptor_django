# Generated by Django 3.0 on 2020-01-14 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_project_project_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
