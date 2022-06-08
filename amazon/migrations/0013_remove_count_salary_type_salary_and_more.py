# Generated by Django 4.0.1 on 2022-04-26 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0012_count_salary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='count_salary',
            name='type_salary',
        ),
        migrations.AddField(
            model_name='count_salary',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='count_salary',
            name='group_teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='amazon.teacher'),
        ),
        migrations.AlterField(
            model_name='count_salary',
            name='salary',
            field=models.IntegerField(),
        ),
    ]