# Generated by Django 4.0.1 on 2022-03-30 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0006_rename_oner_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='level',
        ),
    ]
