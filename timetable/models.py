from django.db import models


class SelectedWorkingHoursByDefault(models.Model):
    tutor_fk = models.ForeignKey('account.ProTutor',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='selected_working_hours_by_default')
    selected_time = models.TextField(default='{"Monday": [], "Tuesday":[], "Wednesday": [], "Thursday": [], '
                                             '"Friday":[], "Saturday":[], "Sunday":[]}')  # {'Monday' : [
    # "8:00-9:00"], }
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class MonthTutorTimetable(models.Model):
    tutor_fk = models.ForeignKey('account.ProTutor',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='selected_working_time_by_default')

    selected_weekdays = models.TextField(default='{}')  # {'1' : ["8:00-9:00"], }
    booked_weekdays = models.TextField(default='{}')  # {'1' : {"8:00-9:00": private_lesson_id}, }

    qty_done_private_lessons = models.PositiveIntegerField(default=0)

    month = models.CharField(default='0', max_length=2)
    year = models.CharField(default='2002', max_length=4)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class MonthStudentTimetable(models.Model):
    progress_fk = models.ForeignKey('access.Progress',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name='month_student_timetable')
    student_fk = models.ForeignKey('account.ProStudent',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='month_student_timetable')
    course_fk = models.ForeignKey('course.Course',
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  related_name='month_student_timetable')

    selected_lesson_days = models.TextField(default='{}')  # {'1' : {"8:00-9:00": private_lesson.id}, }

    qty_finished_private_lessons = models.PositiveIntegerField(default=0)

    month = models.CharField(default='0', max_length=2)
    year = models.CharField(default='2002', max_length=4)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
