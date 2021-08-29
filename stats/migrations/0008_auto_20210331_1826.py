# Generated by Django 3.1.7 on 2021-03-31 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_course_professor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='courses',
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='stats.Student'),
        ),
    ]