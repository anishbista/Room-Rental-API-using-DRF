# Generated by Django 5.0.3 on 2024-03-11 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_alter_amenities_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenities',
            name='ac',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='amenities',
            name='free_cable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='amenities',
            name='free_wifi',
            field=models.BooleanField(default=False),
        ),
    ]
