# Generated by Django 3.1.7 on 2021-04-19 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0040_auto_20210417_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='evalweight',
            name='num',
            field=models.IntegerField(default=0),
        ),
    ]
