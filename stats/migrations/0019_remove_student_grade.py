# Generated by Django 3.1.7 on 2021-04-08 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0018_auto_20210407_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='grade',
        ),
    ]