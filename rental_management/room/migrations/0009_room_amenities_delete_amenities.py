# Generated by Django 5.0.3 on 2024-03-14 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0008_alter_room_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='amenities',
            field=models.CharField(default=52, max_length=250),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Amenities',
        ),
    ]
