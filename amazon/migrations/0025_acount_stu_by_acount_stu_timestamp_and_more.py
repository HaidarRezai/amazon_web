# Generated by Django 4.0.1 on 2022-05-08 04:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0024_acount_stu'),
    ]

    operations = [
        migrations.AddField(
            model_name='acount_stu',
            name='by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='acount_stu',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='acount_stu',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
