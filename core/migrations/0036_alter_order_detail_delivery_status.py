# Generated by Django 5.1.7 on 2025-05-22 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_alter_order_detail_delivery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_detail',
            name='Delivery_Status',
            field=models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='processing', max_length=10),
        ),
    ]
