# Generated by Django 3.1.7 on 2021-03-21 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20210320_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='author',
        ),
        migrations.RemoveField(
            model_name='student',
            name='course',
        ),
        migrations.AddField(
            model_name='course',
            name='student',
            field=models.ForeignKey(blank=True, default=True, on_delete=django.db.models.deletion.CASCADE, to='stats.student'),
            preserve_default=False,
        ),
    ]
