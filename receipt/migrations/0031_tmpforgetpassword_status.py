# Generated by Django 4.1.1 on 2023-05-12 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0030_alter_logo_datey'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmpforgetpassword',
            name='status',
            field=models.CharField(default=0, max_length=200),
        ),
    ]
