# Generated by Django 5.0.2 on 2024-03-08 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeApp', '0001_initial'),
        ('ManagerApp', '0002_remove_task_comments_remove_task_completiondate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='ProjectLead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.employee'),
        ),
    ]
