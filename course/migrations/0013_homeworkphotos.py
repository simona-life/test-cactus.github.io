# Generated by Django 3.1.6 on 2021-04-12 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20210407_1221'),
        ('course', '0012_answerquestion_chose_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeWorkPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lesson_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_photos', to='course.lesson')),
                ('student_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_photos', to='account.prostudent')),
            ],
        ),
    ]
