# Generated by Django 4.2.7 on 2024-03-05 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopciti_app', '0019_remove_customuser_shop_remove_product_shop_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='added_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
