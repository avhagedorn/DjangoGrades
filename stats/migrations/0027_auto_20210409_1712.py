# Generated by Django 3.1.7 on 2021-04-09 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0026_auto_20210409_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experimental',
            name='name',
        ),
        migrations.AddField(
            model_name='experimental',
            name='course',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='stats.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experimental',
            name='evalType',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='stats.evaltype'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='experimental',
            name='data',
            field=models.JSONField(default='`dict`'),
        ),
        migrations.AlterField(
            model_name='student',
            name='data',
            field=models.JSONField(default='`dict`'),
        ),
    ]
