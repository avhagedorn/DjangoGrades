# Generated by Django 3.1.7 on 2021-04-09 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0023_auto_20210409_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseavg',
            name='assignmentType',
        ),
        migrations.AddField(
            model_name='courseavg',
            name='title',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='data',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
