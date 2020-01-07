# Generated by Django 3.0 on 2020-01-03 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcriptions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcriptiontext',
            name='status',
            field=models.CharField(choices=[('approved', 'Approved'), ('denied', 'Denied'), ('pending', 'Pending')], default='approved', max_length=250),
            preserve_default=False,
        ),
    ]