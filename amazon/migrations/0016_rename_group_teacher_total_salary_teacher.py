# Generated by Django 4.0.1 on 2022-04-26 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0015_rename_salary_total_salary_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='total_salary',
            old_name='group_teacher',
            new_name='teacher',
        ),
    ]
