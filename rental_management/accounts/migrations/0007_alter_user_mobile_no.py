# Generated by Django 5.0.3 on 2024-03-10 07:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_otp_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_no',
            field=models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]