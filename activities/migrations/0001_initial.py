# Generated by Django 3.2.3 on 2021-06-25 15:53

import activities.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('image', models.ImageField(upload_to=activities.models.activity_image_path)),
                ('description', models.TextField(max_length=1500)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]