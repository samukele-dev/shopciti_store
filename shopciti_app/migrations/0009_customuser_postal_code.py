# Generated by Django 4.2.7 on 2024-02-29 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopciti_app', '0008_customuser_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='postal_code',
            field=models.CharField(default='000000000', max_length=20),
        ),
    ]
