# Generated by Django 4.1.1 on 2023-05-09 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0022_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='key',
            name='username',
            field=models.CharField(default='admin', max_length=200),
        ),
    ]
