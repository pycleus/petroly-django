# Generated by Django 3.1.7 on 2021-02-26 10:53

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0003_remove_instructor_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='profile_pic',
            field=cloudinary.models.CloudinaryField(blank=True, default='https://res.cloudinary.com/ammar-faifi/image/upload/v1614314169/sample.jpg', max_length=255, verbose_name='image'),
        ),
    ]