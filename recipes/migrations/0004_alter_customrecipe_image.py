# Generated by Django 4.0.5 on 2024-02-07 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_customrecipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customrecipe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='recipe_images'),
        ),
    ]
