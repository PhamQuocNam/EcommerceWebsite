# Generated by Django 5.1.7 on 2025-04-18 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0009_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='image/default.jpg', upload_to='image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
