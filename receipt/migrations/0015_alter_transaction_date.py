# Generated by Django 4.1.1 on 2023-03-16 17:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0014_remove_transaction_date2_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 16, 18, 55, 50, 5613)),
        ),
    ]
