# Generated by Django 4.0.1 on 2022-04-26 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0013_remove_count_salary_type_salary_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Count_salary',
            new_name='Total_salary',
        ),
    ]
