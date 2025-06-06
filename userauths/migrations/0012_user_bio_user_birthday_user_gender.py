# Generated by Django 5.1.7 on 2025-04-18 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0011_remove_user_bio_remove_user_birthday_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Bio',
            field=models.CharField(default='...', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='Birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='Gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='other', max_length=10),
        ),
    ]
