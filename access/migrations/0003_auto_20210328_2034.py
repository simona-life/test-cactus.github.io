# Generated by Django 3.1.6 on 2021-03-28 20:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_auto_20210328_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='end_sub_data',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='progress',
            name='start_sub_data',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
