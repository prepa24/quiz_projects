# Generated by Django 5.0.7 on 2024-09-05 18:34

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_imagesettings_question_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.AddField(
            model_name='question',
            name='image1',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[500, 300], upload_to='question_images'),
        ),
    ]