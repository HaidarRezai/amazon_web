# Generated by Django 4.0.4 on 2022-05-20 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0030_alter_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]