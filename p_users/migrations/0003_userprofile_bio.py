# Generated by Django 5.0.7 on 2024-11-10 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_users', '0002_remove_userprofile_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(default=1, max_length=500),
        ),
    ]
