# Generated by Django 3.1.6 on 2021-04-24 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_course_include_month_private_lessons_default_fk'),
        ('access', '0008_auto_20210421_2100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='progress',
            old_name='end_sub_data',
            new_name='end_sub_date',
        ),
        migrations.RenameField(
            model_name='progress',
            old_name='start_sub_data',
            new_name='start_sub_date',
        ),
        migrations.AddField(
            model_name='progress',
            name='include_month_private_lessons_current',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='progress',
            name='include_month_private_lessons_default_fk',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='course.course'),
            preserve_default=False,
        ),
    ]
