# Generated by Django 3.1.6 on 2021-04-07 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='type_lesson',
            field=models.CharField(choices=[('class_work', 'Класна робота'), ('home_work', 'Домашня робота'), ('explanation_home_work', 'Пояснення домашньої роботи'), ('control_work', 'Контрольна робота')], default='class_work', max_length=30),
        ),
    ]