# Generated by Django 5.0.6 on 2024-08-14 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_alter_paymentmethod_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='organization',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='work_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
    ]
