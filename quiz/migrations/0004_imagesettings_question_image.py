# Generated by Django 5.0.7 on 2024-08-23 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quizsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.PositiveIntegerField(default=100)),
                ('height', models.PositiveIntegerField(default=100)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='question_images/'),
        ),
    ]
