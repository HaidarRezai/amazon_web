# Generated by Django 4.0.1 on 2022-04-08 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0010_remove_attendance_group_student_attendance_group'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]