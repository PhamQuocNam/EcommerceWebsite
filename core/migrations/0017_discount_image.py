# Generated by Django 5.1.7 on 2025-04-16 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_rename_address1_address_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='Image',
            field=models.ImageField(default='campaign.jpg', upload_to='campaign-image'),
        ),
    ]
