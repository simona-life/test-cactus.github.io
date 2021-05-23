from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class PrivateLesson(models.Model):
    tutor_fk = models.ForeignKey('account.ProTutor',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='private_lessons')
    student_fk = models.ForeignKey('account.ProStudent',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='private_lessons')
    progress_fk = models.ForeignKey('access.Progress',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name='private_lessons')

    title = models.CharField(default='', max_length=60)
    report_tutor = models.TextField(default='')
    video_lesson = models.FileField(upload_to="video/private_lessons/%y")
    points = models.PositiveIntegerField(default=0,
                                         validators=[
                                             MinValueValidator(0),
                                             MaxValueValidator(10),
                                         ])

    lesson_date = models.DateField(default='01.01.2002')
    lesson_time = models.CharField(default='7:00-8:00', max_length=20)
    checked_by_head_teacher = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-lesson_date']
