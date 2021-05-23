import json
from django import template
from django.utils.datetime_safe import date

from access.models import Progress
from course.models import (Course,
                           Question,
                           AnswerQuestion)

register = template.Library()


@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None


@register.filter
def check_access_lesson(my_dict, my_key):
    try:
        if my_dict[str(my_key)] == True:
            return True
        else:
            return False
    except:
        return False


@register.filter
def bought_course_check(id_course, student):
    try:
        Progress.objects.get(student_fk=student, id_course=id_course)
        return True
    except Progress.DoesNotExist:
        return False


@register.filter
def end_sub_date(student, course_id):
    none_date = 'Студент ще не проходив даний курс'
    for progress in student.progresses.all():
        if progress.id_course == course_id:
            return progress.end_sub_data
    return none_date


@register.filter
def status_student_in_course(student, course_id):
    status_active = 'Активний'
    status_pause = 'Пауза'
    status_inactive = 'Не активний'
    for progress in student.progresses.all():
        if progress.id_course == course_id:
            if progress.end_sub_data > date.today():
                return status_active
            else:
                return status_pause
    return status_inactive


@register.filter
def get_username_by_progress(progress):
    student = progress.student_fk
    # cid = progress.id_course
    username = student.profile.user.username
    return username


@register.filter
def get_names_by_progress(progress):
    student = progress.student_fk
    # cid = progress.id_course
    first_name = student.profile.user.first_name
    last_name = student.profile.user.last_name
    names = str(first_name) + str(last_name)
    return names


@register.filter
def get_title_course_by_id(cid):
    title_course = Course.objects.get(id=cid)
    return title_course


@register.filter
def open_check_lesson(progress, lid):
    lessons_opened = json.loads(progress.lessons_opened)
    if lessons_opened[str(lid)]:
        return True
    else:
        return False


@register.filter
def percent_passed_lessons(progress):
    all_lessons = json.loads(progress.lessons_opened)
    all_lessons_counter = len(all_lessons)

    opened_counter = 0
    for lesson_id in all_lessons:
        if all_lessons[lesson_id]:
            opened_counter += 1

    percent = round(opened_counter*100/all_lessons_counter)
    return percent


@register.filter
def current_qty_tutor_students(tutor):
    qty_students = len(tutor.progresses.all())
    return qty_students


@register.filter
def get_chose_answer(question, student):
    current_answer = AnswerQuestion.objects.filter(student_fk=student, question_fk=question)[0]
    return current_answer.chose_answer


@register.filter
def get_points_by_answer(question, student):
    current_answer = AnswerQuestion.objects.filter(student_fk=student, question_fk=question)[0]
    if question.correct_answer == current_answer.chose_answer:
        return question.points
    else:
        return 0


@register.filter
def check_points_lesson_d(progress, lid):
    points_progress = json.loads(progress.points_progress)
    try:
        user_total_points = points_progress[str(lid)+'d']
        return True
    except KeyError:
        return False


@register.filter
def get_points_lesson_d(progress, lid):
    points_progress = json.loads(progress.points_progress)
    try:
        user_total_points = points_progress[str(lid)+'d']
        return user_total_points
    except KeyError:
        return False
