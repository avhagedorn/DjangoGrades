# Generated by Django 3.1.7 on 2021-04-18 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0036_auto_20210417_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='grade_dist',
            field=models.JSONField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]'),
        ),
    ]
