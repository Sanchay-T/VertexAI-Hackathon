# Generated by Django 4.2.3 on 2023-07-23 10:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="company",
            name="company_information",
        ),
        migrations.RemoveField(
            model_name="jobpost",
            name="job_salary",
        ),
        migrations.RemoveField(
            model_name="jobpost",
            name="salary_range",
        ),
        migrations.AddField(
            model_name="jobpost",
            name="company_information",
            field=models.TextField(default=None, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="jobpost",
            name="job_salary_range",
            field=models.CharField(default=None, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="jobapplication",
            name="application_status",
            field=models.CharField(
                choices=[
                    ("Applied", "Applied"),
                    ("Rejected", "Rejected"),
                    ("Interview Stage", "Interview Stage"),
                    ("Job Offered", "Job Offered"),
                ],
                default="Applied",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="jobapplication",
            name="hiring_decision",
            field=models.CharField(
                choices=[
                    ("Hired", "Hired"),
                    ("Rejected", "Rejected"),
                    ("Pending", "Pending"),
                ],
                default="Pending",
                max_length=250,
                null=True,
            ),
        ),
    ]