# Generated by Django 3.0.8 on 2020-11-20 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_product_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discountInfo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
