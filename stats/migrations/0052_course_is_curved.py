# Generated by Django 3.1.7 on 2021-06-28 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0051_auto_20210626_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_curved',
            field=models.BooleanField(default=False),
        ),
    ]
