# Generated by Django 3.2.3 on 2021-06-22 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_alter_booking_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ('-date_from',)},
        ),
    ]