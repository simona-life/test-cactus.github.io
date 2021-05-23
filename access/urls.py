from django.urls import path

from access.views import (buy_course,
                          buy_course_by_guest,
                          buy_course_by_parent,
                          buy_course_by_student,
                          buy_course_by_parent_student,
                          buy_additional_private_lessons_by_parent,
                          buy_additional_private_lessons_by_student)


urlpatterns = [
    path('<int:cid>/buy-course', buy_course, name='buy_course'),
    path('<int:cid>/guest-buy-course', buy_course_by_guest, name='buy_course_by_guest'),
    path('<int:cid>/parent-buy-course', buy_course_by_parent, name='buy_course_by_parent'),
    path('<int:cid>/student<int:sid>/buy/', buy_course_by_parent_student, name='buy_course_by_parent_student'),
    path('<int:cid>/buy/', buy_course_by_student, name='buy_course_by_student'),

    path('<int:cid>/buy_additional_private_lessons_by_student/', buy_additional_private_lessons_by_student, name='buy_additional_private_lessons_by_student'),
    path('<int:cid>/buy_additional_private_lessons_by_parent/<int:sid>/', buy_additional_private_lessons_by_parent, name='buy_additional_private_lessons_by_parent'),
]

