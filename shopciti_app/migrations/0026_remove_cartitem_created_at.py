# Generated by Django 4.2.7 on 2024-03-08 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopciti_app', '0025_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='created_at',
        ),
    ]
