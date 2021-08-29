# Generated by Django 3.1.7 on 2021-05-15 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0046_student_letter_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='detailed',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='letter_grade',
            field=models.CharField(default='-', max_length=2),
        ),
    ]