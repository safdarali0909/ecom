# Generated by Django 5.0.6 on 2024-08-15 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
