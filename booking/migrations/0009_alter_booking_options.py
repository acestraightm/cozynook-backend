# Generated by Django 3.2.3 on 2021-06-21 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_booking'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ('date_from',)},
        ),
    ]
