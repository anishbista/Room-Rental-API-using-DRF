# Generated by Django 5.0.3 on 2024-03-14 04:32

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
                ('landlord_email', models.EmailField(max_length=255, verbose_name='email')),
                ('customer_email', models.EmailField(max_length=255, verbose_name='email')),
                ('name', models.CharField(max_length=250)),
                ('phone_no', models.CharField(max_length=10)),
                ('message', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]