# Generated by Django 5.0.6 on 2024-08-15 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
