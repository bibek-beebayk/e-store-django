# Generated by Django 3.2.9 on 2021-11-29 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20211129_0802'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='birth_data',
            new_name='birth_date',
        ),
    ]
