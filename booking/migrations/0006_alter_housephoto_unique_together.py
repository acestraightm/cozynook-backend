# Generated by Django 3.2.3 on 2021-06-15 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_alter_housephoto_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='housephoto',
            unique_together=set(),
        ),
    ]
