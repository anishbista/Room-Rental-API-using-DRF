# Generated by Django 5.0.3 on 2024-03-11 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0006_room_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='image',
        ),
    ]