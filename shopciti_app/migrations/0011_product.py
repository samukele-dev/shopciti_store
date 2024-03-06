# Generated by Django 4.2.7 on 2024-02-29 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopciti_app', '0010_rename_shop_customuser_shop_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='product_images/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
