# Generated by Django 3.1.7 on 2021-04-09 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0024_auto_20210409_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseavg',
            name='title',
        ),
        migrations.AddField(
            model_name='courseavg',
            name='assignmentType',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='stats.evaltype'),
            preserve_default=False,
        ),
    ]
