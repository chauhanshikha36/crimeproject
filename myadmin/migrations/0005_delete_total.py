# Generated by Django 4.0.3 on 2022-04-12 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0004_remove_total_area_total_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Total',
        ),
    ]