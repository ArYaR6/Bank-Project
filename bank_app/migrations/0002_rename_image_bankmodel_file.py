# Generated by Django 4.2.1 on 2023-07-01 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bankmodel',
            old_name='image',
            new_name='file',
        ),
    ]
