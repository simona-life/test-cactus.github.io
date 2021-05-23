import datetime
from django.db import models
from account.models import (ProTutor,
                            ProStudent,
                            ProParent)


class Payment(models.Model):
    # progress_fk = models.ForeignKey('access.Progress',
    #                                 on_delete=models.,
    #                                 blank=True,
    #                                 related_name='payments')
    # MORE FIELDS
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Progress(models.Model):
    student_fk = models.ForeignKey('account.ProStudent',
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   related_name='progresses')
    tutor_fk = models.ForeignKey('account.ProTutor',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='students_progresses')
    id_course = models.IntegerField(default=0)
    lessons_opened = models.TextField(default='{}')  # lesson_id : True/False
    points_progress = models.TextField(default='{}')  # lesson_id : points
    points = models.PositiveIntegerField(default=0)

    start_sub_date = models.DateField(default=datetime.date.today)
    end_sub_date = models.DateField(default=datetime.date.today)

    is_active = models.BooleanField(default=True)

    include_month_private_lessons_include_default = models.PositiveIntegerField(default=0)
    include_month_private_lessons_current = models.PositiveIntegerField(default=0)  # delete after ending end_sub_date

    qty_bought_private_lessons = models.PositiveIntegerField(default=0)
    qty_finished_private_lessons = models.PositiveIntegerField(default=0)
