# Generated by Django 4.0.1 on 2022-03-28 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0003_group_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'Admin'), (2, 'HOD'), (4, 'Teacher')], default=1, max_length=50),
        ),
        migrations.CreateModel(
            name='Oner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(max_length=50)),
                ('phone_one', models.CharField(max_length=50)),
                ('phone_tow', models.CharField(max_length=50)),
                ('degree_edu', models.CharField(max_length=50)),
                ('address_one', models.CharField(max_length=50)),
                ('address_tow', models.CharField(max_length=50)),
                ('idcord', models.CharField(max_length=50)),
                ('level', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
