from django.urls import path

from course.views import (all_courses,
                          course_details,
                          user_course_details,
                          student_course_details,
                          admin_course_details,
                          result_hw_lesson,
                          lesson)

urlpatterns = [
    path('<int:cid>/', course_details, name='course_details'),
    path('<int:cid>/student/', student_course_details, name='student_course_details'),
    path('<int:cid>/staff/', admin_course_details, name='admin_course_details'),
    path('<int:cid>/user/', user_course_details, name='user_course_details'),
    path('<int:cid>/lesson/<int:lid>/', lesson, name='lesson'),
    path('student/<int:sid>/result_hw_lesson/<int:lid>/', result_hw_lesson, name='result_hw_lesson'),
]
