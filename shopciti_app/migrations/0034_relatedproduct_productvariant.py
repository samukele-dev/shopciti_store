# Generated by Django 4.2.7 on 2024-03-13 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopciti_app', '0033_remove_category_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='shopciti_app.product')),
                ('related_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopciti_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_variant_images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='shopciti_app.product')),
            ],
        ),
    ]
