# Generated by Django 5.0.6 on 2024-08-09 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_remove_paymentmethod_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmethod',
            name='upi_id',
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='method',
            field=models.CharField(choices=[('credit_card', 'Credit or Debit Card'), ('net_banking', 'Net Banking'), ('upi', 'UPI'), ('emi', 'EMI'), ('cod', 'Cash on Delivery')], max_length=20),
        ),
    ]
