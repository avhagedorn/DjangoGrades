# Generated by Django 3.1.7 on 2021-05-11 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0041_evalweight_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentavg',
            name='course',
        ),
        migrations.RemoveField(
            model_name='assignmentavg',
            name='evalType',
        ),
        migrations.RemoveField(
            model_name='courseavg',
            name='assignmentType',
        ),
        migrations.RemoveField(
            model_name='courseavg',
            name='course',
        ),
        migrations.DeleteModel(
            name='Assignment',
        ),
        migrations.DeleteModel(
            name='AssignmentAvg',
        ),
        migrations.DeleteModel(
            name='CourseAvg',
        ),
    ]