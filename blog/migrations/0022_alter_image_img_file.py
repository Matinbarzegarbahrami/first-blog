# Generated by Django 5.2 on 2025-04-20 11:49

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_alter_image_img_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='img_file',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
