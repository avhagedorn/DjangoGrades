# Generated by Django 3.1.7 on 2021-04-09 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0028_auto_20210409_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentavg',
            name='data',
            field=models.JSONField(default='{}'),
        ),
        migrations.AlterField(
            model_name='student',
            name='data',
            field=models.JSONField(default='{}'),
        ),
    ]
