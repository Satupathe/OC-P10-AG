# Generated by Django 3.2.8 on 2021-10-21 12:46

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_comments_contributors_issues_projects'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='users',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='projects',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
