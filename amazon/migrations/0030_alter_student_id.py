# Generated by Django 4.0.4 on 2022-05-20 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0029_alter_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.CharField(max_length=19, primary_key=True, serialize=False),
        ),
    ]
