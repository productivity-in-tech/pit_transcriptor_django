# Generated by Django 3.0 on 2020-01-27 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcriptions', '0005_auto_20200127_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcriptionedit',
            name='edited_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
