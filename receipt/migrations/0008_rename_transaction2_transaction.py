# Generated by Django 4.1.1 on 2023-03-13 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0007_signature2'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transaction2',
            new_name='Transaction',
        ),
    ]