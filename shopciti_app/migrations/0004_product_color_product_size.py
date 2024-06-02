# Generated by Django 4.1.2 on 2024-05-26 02:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shopciti_app', '0003_alter_order_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(choices=[('white', 'white'), ('black', 'black'), ('red', 'red'), ('blue', 'blue'), ('green', 'Green'), ('yellow', 'yellow'), ('other', 'other')], default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('Xlarge', 'XLarge')], default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
    ]
