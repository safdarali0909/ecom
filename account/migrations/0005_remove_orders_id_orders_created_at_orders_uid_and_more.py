# Generated by Django 5.0.6 on 2024-08-03 23:52

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_orders_price_alter_orders_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='id',
        ),
        migrations.AddField(
            model_name='orders',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='orders',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='upi_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='OrderSummary',
        ),
    ]
