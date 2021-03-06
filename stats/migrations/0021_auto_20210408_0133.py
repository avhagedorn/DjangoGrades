# Generated by Django 3.1.7 on 2021-04-08 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0020_student_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaltype',
            name='maxPts',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='evaltype',
            name='weight',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.SmallIntegerField(),
        ),
    ]
