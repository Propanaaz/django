# Generated by Django 4.1.1 on 2023-05-12 18:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0029_tmpforgetpassword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logo',
            name='datey',
            field=models.DateField(default=datetime.date(2023, 6, 11)),
        ),
    ]