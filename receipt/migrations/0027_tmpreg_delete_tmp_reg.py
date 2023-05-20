# Generated by Django 4.1.1 on 2023-12-10 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0026_alter_logo_datey_tmp_reg'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tmpreg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('businessname', models.CharField(max_length=200)),
                ('businessaddress', models.CharField(default='Your Address Here', max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='tmp_reg',
        ),
    ]