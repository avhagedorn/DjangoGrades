# Generated by Django 3.1.7 on 2021-06-27 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0050_course_show_predictive_tools'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
