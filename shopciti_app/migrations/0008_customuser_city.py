# Generated by Django 4.2.7 on 2024-02-29 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopciti_app', '0007_shop_city_shop_contact_email_shop_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='city',
            field=models.CharField(default='South Africa', max_length=100),
        ),
    ]
