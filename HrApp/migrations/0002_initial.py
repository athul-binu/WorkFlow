# Generated by Django 5.0.2 on 2024-03-04 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('HrApp', '0001_initial'),
        ('ManagerApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='RequestID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ManagerApp.recruitmentrequest'),
        ),
        migrations.AddField(
            model_name='performancereview',
            name='ReviewerID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HrApp.hr'),
        ),
        migrations.AddField(
            model_name='recruitmentapplication',
            name='ApplicantID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HrApp.applicant'),
        ),
        migrations.AddField(
            model_name='recruitmentapplication',
            name='ApplicationID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HrApp.jobapplication'),
        ),
        migrations.AddField(
            model_name='performancereview',
            name='RecruitmentApplicationID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HrApp.recruitmentapplication'),
        ),
    ]