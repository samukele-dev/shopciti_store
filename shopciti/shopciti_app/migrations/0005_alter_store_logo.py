# Generated by Django 4.1.2 on 2023-10-03 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopciti_app', '0004_remove_store_profile_image_store_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='logo',
            field=models.ImageField(default='static/img/1.png', upload_to='store_logos/'),
        ),
    ]
