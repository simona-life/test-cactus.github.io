# Generated by Django 3.1.6 on 2021-03-03 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('course', '0002_auto_20210303_2102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['order']},
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='topics',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='courses',
        ),
        migrations.AddField(
            model_name='lesson',
            name='topic_fk',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='course.topic'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='course_fk',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='course.course'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ('Text', 'video', 'image', 'file')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='content',
            name='lesson_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='course.lesson'),
        ),
    ]
