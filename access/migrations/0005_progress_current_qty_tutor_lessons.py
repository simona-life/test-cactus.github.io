# Generated by Django 3.1.6 on 2021-04-07 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0004_auto_20210407_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='current_qty_tutor_lessons',
            field=models.PositiveIntegerField(default=4),
        ),
    ]