# Generated by Django 4.1.1 on 2023-04-08 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0020_delete_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistration2',
            name='businessaddress',
            field=models.CharField(default='Your Address Here', max_length=200),
        ),
    ]