# Generated by Django 3.1.6 on 2021-04-26 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0009_monthtutortimetable_qty_done_lessons'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monthtutortimetable',
            old_name='qty_done_lessons',
            new_name='qty_done_private_lessons',
        ),
    ]
