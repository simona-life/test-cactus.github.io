from django.urls import path

from studprogress.views import (student_progress_by_tutor,
                                student_progress_by_parent,
                                student_progress_by_head_teacher)


urlpatterns = [
    path('<int:cid>/student/<int:sid>/student_progress_by_head_teacher/', student_progress_by_head_teacher, name='student_progress_by_head_teacher'),
    path('<int:cid>/student/<int:sid>/student_progress_by_tutor/', student_progress_by_tutor, name='student_progress_by_tutor'),
    path('<int:cid>/student/<int:sid>/student_progress/', student_progress_by_parent, name='student_progress_by_parent'),
]
