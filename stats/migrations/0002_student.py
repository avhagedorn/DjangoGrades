# Generated by Django 3.1.7 on 2021-03-21 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=15)),
                ('last', models.CharField(max_length=15)),
                ('courses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.course')),
            ],
        ),
    ]