# Generated by Django 3.1.6 on 2021-04-24 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_course_include_month_private_lessons_default_fk'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='include_month_private_lessons_default_fk',
            new_name='include_month_private_lessons_default',
        ),
    ]
