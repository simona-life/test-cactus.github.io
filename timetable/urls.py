from django.urls import path

from timetable.views import (date_by_student,
                             change_month_timetable_tutor,
                             change_month_timetable_student)


urlpatterns = [
    path('change_month_timetable_tutor/', change_month_timetable_tutor, name='change_month_timetable_tutor'),
    path('<int:cid>/change_month_timetable_student/', change_month_timetable_student, name='change_month_timetable_student'),
    path('<int:date_day>/date_by_student/<int:mtb_id>/', date_by_student, name='date_by_student'),
]
