# Generated by Django 4.1.3 on 2023-01-07 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalproject', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
