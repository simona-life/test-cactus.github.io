# Generated by Django 3.1.6 on 2021-04-18 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_auto_20210418_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectedworkinghoursbydefault',
            name='selected_time',
            field=models.TextField(default='{"Monday": [], "Tuesday":[], "Wednesday": [], "Thursday": [], "Friday":[], "Saturday":[], "Sunday":[]}'),
        ),
    ]
