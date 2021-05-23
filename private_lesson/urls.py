from django.urls import path

from private_lesson.views import (private_lesson_view,
                                  private_lesson_view_by_tutor,
                                  private_lesson_view_by_student,
                                  private_lesson_view_by_head_teacher,
                                  result_private_lesson_view,
                                  result_private_lesson_view_by_tutor,
                                  result_private_lesson_view_by_head_teacher,
                                  result_private_lesson_view_by_student,
                                  result_private_lesson_view_by_parent,
                                  all_private_lessons_in_course_by_parent,
                                  all_private_lessons_in_course_by_tutor)

urlpatterns = [
    path('<int:lid>/private_lesson_view/', private_lesson_view, name='private_lesson_view'),
    path('by_student/<int:lid>/', private_lesson_view_by_student, name='private_lesson_view_by_student'),
    path('by_tutor/<int:lid>/', private_lesson_view_by_tutor, name='private_lesson_view_by_tutor'),
    path('by_head_teacher/<int:lid>/', private_lesson_view_by_head_teacher, name='private_lesson_view_by_head_teacher'),

    path('<int:lid>/result_private_lesson_view/', result_private_lesson_view, name='result_private_lesson_view'),
    path('by_student/<int:lid>/', result_private_lesson_view_by_student, name='result_private_lesson_view_by_student'),
    path('by_tutor/<int:lid>/', result_private_lesson_view_by_tutor, name='result_private_lesson_view_by_tutor'),
    path('by_head_teacher/<int:lid>/', result_private_lesson_view_by_head_teacher, name='result_private_lesson_view_by_head_teacher'),
    path('<int:lid>/result_private_lesson_view_by_parent/<int:pid>/', result_private_lesson_view_by_parent, name='result_private_lesson_view_by_parent'),

    path('all_private_lessons_in_course_by_tutor/', all_private_lessons_in_course_by_tutor, name='all_private_lessons_in_course_by_tutor'),
    path('all_private_lessons_in_course_by_parent/', all_private_lessons_in_course_by_parent, name='all_private_lessons_in_course_by_parent'),
]
