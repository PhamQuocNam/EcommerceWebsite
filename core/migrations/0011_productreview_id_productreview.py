# Generated by Django 5.1.7 on 2025-04-03 07:18

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_product_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='ID_ProductReview',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=20, prefix='ORDER', unique=True),
        ),
    ]
