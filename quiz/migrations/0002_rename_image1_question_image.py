# Generated by Django 5.0.7 on 2024-11-03 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='image1',
            new_name='image',
        ),
    ]
