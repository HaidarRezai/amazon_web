# Generated by Django 4.0.1 on 2022-05-09 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0025_acount_stu_by_acount_stu_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='fees',
            field=models.IntegerField(),
        ),
    ]
