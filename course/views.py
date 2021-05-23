import json
import calendar
from datetime import datetime
from django.utils.datetime_safe import date

from django.shortcuts import (render,
                              redirect,
                              get_object_or_404)

from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from access.decorators import login_required_message, student_type_only

from access.views import (check_open_lesson,
                          check_date_access_to_course)
from course.models import (Course,
                           Lesson,
                           Question,
                           AnswerQuestion,
                           HomeWorkPhotos)
from access.models import (Progress)
from account.models import (Profile,
                            ProStudent)
from timetable.models import MonthStudentTimetable
from private_lesson.models import PrivateLesson


def all_courses(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        if profile.type_user == 'student':
            student = ProStudent.objects.get(profile=profile)
            progresses = Progress.objects.filter(student_fk=student)
            context = {
                'courses': Course.objects.filter(finished=True),
                'progresses': progresses,
                'student': student,
            }
            return render(request, 'course/all_courses_student.html', context)
        else:
            context = {
                'courses': Course.objects.filter(finished=True)
            }
            return render(request, 'course/all_courses_user.html', context)
    else:
        context = {
            'courses': Course.objects.filter(finished=True)
        }
        return render(request, 'course/all_courses_user.html', context)


def course_details(request, cid):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        if profile.type_user == 'student':
            return HttpResponseRedirect(reverse('student_course_details', kwargs={'cid': cid}))
        elif profile.type_user == 'tutor' or profile.type_user == 'head-teacher':
            return HttpResponseRedirect(reverse('admin_course_details', kwargs={'cid': cid}))
        else:
            return HttpResponseRedirect(reverse('user_course_details', kwargs={'cid': cid}))
    else:
        return HttpResponseRedirect(reverse('user_course_details', kwargs={'cid': cid}))


@login_required_message(message='Для того, щоб купити курс потрібно увійти у акаунт!')
@login_required
@student_type_only
def student_course_details(request, cid):
    action = request.POST.get('action')
    if request.POST and action == 'Купити доступ':
        return redirect('buy_course', cid)

    cid_course = get_object_or_404(Course, id=cid)
    profile = Profile.objects.get(user=request.user)
    student = ProStudent.objects.get(profile=profile)
    try:
        progress = Progress.objects.get(student_fk=student, id_course=cid)
    except Progress.DoesNotExist:
        context = {
            'course': cid_course,
            'topics': cid_course.topics.all(),
        }
        return render(request, 'course/view_course_user.html', context)
    # check date access
    if check_date_access_to_course(progress):
        access_lessons = json.loads(progress.lessons_opened)

        progress = Progress.objects.get(student_fk=request.user.profile.prostudent, id_course=cid)
        current_year = datetime.today().year
        current_month = datetime.today().month

        today_day = date.today().day
        today_weekday = date.today().weekday()

        try:
            month_timetable_student = MonthStudentTimetable.objects.get(month=current_month, year=current_year,
                                                                        progress_fk=progress)
            booked_weekdays = json.loads(month_timetable_student.selected_lesson_days)
        except MonthStudentTimetable.DoesNotExist:
            booked_weekdays = []

        max_day_month = calendar.monthrange(current_year, current_month)[1]
        private_lessons = PrivateLesson.objects.filter(progress_fk=progress)
        if len(private_lessons) == 0:
            private_lessons = 0

        context = {
            'today_day': today_day,
            'today_weekday': today_weekday,
            'current_month': current_month,
            'booked_weekdays': booked_weekdays,
            'private_lessons': private_lessons,

            'access_lessons': access_lessons,
            'course': cid_course,
            'topics': cid_course.topics.all(),
        }
        return render(request, 'course/true_access_data_view_course_student.html', context)
    else:
        context = {
            'course': cid_course,
            'topics': cid_course.topics.all(),
        }
        return render(request, 'course/false_access_data_view_course_student.html', context)


@login_required_message(message='Для того, щоб купити курс потрібно увійти у акаунт!')
@login_required
def admin_course_details(request, cid):
    action = request.POST.get('action')
    if request.POST and action == 'Купити доступ':
        return redirect('buy_course', cid)

    cid_course = get_object_or_404(Course, id=cid)
    context = {
        'course': cid_course,
        'topics': cid_course.topics.all(),
    }
    return render(request, 'course/view_course_admin.html', context)


def user_course_details(request, cid):
    action = request.POST.get('action')
    if request.POST and action == 'Купити доступ':
        # save link into session
        request.session.set_expiry(1200)
        request.session['next_url'] = request.META.get('HTTP_REFERER')
        return redirect('buy_course', cid)

    cid_course = get_object_or_404(Course, id=cid)
    context = {
        'course': cid_course,
        'topics': cid_course.topics.all(),
    }
    return render(request, 'course/view_course_user.html', context)


@login_required
def lesson(request, cid, lid):
    profile = get_object_or_404(Profile, user=request.user)
    lid_lesson = get_object_or_404(Lesson, id=lid)

    action = request.POST.get('action')

    if request.POST and action == 'Відправити':
        student = ProStudent.objects.get(profile=profile)
        progress = get_object_or_404(Progress, student_fk=student)

        user_total_points = 0
        max_total_points = 0

        questions = lid_lesson.questions.all()

        for question in questions:
            max_total_points += question.points

        for answer in request.POST:
            if "choice_question_" in answer:
                question_id = answer[-1]
                user_answer_question_id = request.POST['choice_question_' + str(question_id)]
                question = lid_lesson.questions.get(id=question_id)
                correct_answer_question_id = question.correct_answer
                question_points = question.points
                if user_answer_question_id == correct_answer_question_id:
                    AnswerQuestion.objects.create(points=question_points,
                                                  student_fk=student,
                                                  question_fk=question,
                                                  chose_answer=user_answer_question_id)

                    user_total_points += question_points
                else:
                    AnswerQuestion.objects.create(points=0,
                                                  student_fk=student,
                                                  question_fk=question,
                                                  chose_answer=user_answer_question_id)

        for photo in request.FILES.getlist('photo'):
            HomeWorkPhotos.objects.create(image=photo, student_fk=student, lesson_fk=lid_lesson)

        # save questions points
        points_progress = json.loads(progress.points_progress)
        points_progress[str(lid)] = user_total_points
        points_progress = json.dumps(points_progress)
        progress.points_progress = points_progress

        progress.points = progress.points + user_total_points
        progress.save()

    if profile.type_user == 'student':
        student = ProStudent.objects.get(profile=profile)
        progress = get_object_or_404(Progress, student_fk=student, id_course=cid)
        # check date access
        if check_date_access_to_course(progress):
            # check open current lesson
            if check_open_lesson(progress, lid):
                contents = lid_lesson.contents.all()
                # lesson does not have tests (class work)
                if len(lid_lesson.questions.all()) == 0:
                    context = {
                        'lesson': lid_lesson,
                        'contents': contents,
                    }
                # lesson has tests
                else:
                    # student has answers
                    if check_answers(lid, student.id):
                        return HttpResponseRedirect(reverse('result_hw_lesson', kwargs={'sid': student.id, 'lid': lid}))
                    # student does not have answers
                    else:
                        context = {
                            'lesson': lid_lesson,
                            'contents': contents,
                            'questions': lid_lesson.questions.all(),
                        }
                return render(request, 'course/view_lesson_student.html', context)
            else:
                messages.warning(request,
                                 "На жаль, Ви не маєте доступу до цього уроку. Виконайте попередні домашні роботи або "
                                 "зверніться до Тьютора!")
                return HttpResponseRedirect(reverse('course_details', kwargs={'cid': cid}))
        else:
            messages.warning(request, "На жаль, Ви не маєте доступу до цього курсу. Ви можете придбати підписку нижче!")
            cid_course = get_object_or_404(Course, id=cid)
            context = {
                'course': cid_course,
                'topics': cid_course.topics.all(),
            }
            return render(request, 'course/false_access_data_view_course_student.html', context)
    elif profile.type_user == 'tutor' or profile.type_user == 'head-teacher':
        contents = lid_lesson.contents.all()
        context = {
            'lesson': lid_lesson,
            'contents': contents,
        }
        return render(request, 'course/view_lesson_admin.html', context)
    else:
        messages.warning(request, "На жаль, Ви не маєте доступу до цього курсу. Ви можете придбати підписку нижче!")
        return HttpResponseRedirect(reverse('course_details', kwargs={'cid': cid}))


@login_required
def result_hw_lesson(request, sid, lid):
    profile = get_object_or_404(Profile, user=request.user)
    student = ProStudent.objects.get(profile=profile)
    progress = get_object_or_404(Progress, student_fk=student)
    lid_lesson = Lesson.objects.get(id=lid)

    hw_images = HomeWorkPhotos.objects.filter(student_fk=student, lesson_fk=lid_lesson)
    questions = lid_lesson.questions.all()
    contents = lid_lesson.contents.all()

    points_progress = json.loads(progress.points_progress)

    action = request.POST.get('action')

    if request.POST:
        if action == 'Оцінити роботу':
            points_tutor_mark = request.POST['points']
            points_progress[str(lid)+'d'] = points_tutor_mark
            points_progress = json.dumps(points_progress)
            progress.points_progress = points_progress
            progress.points += points_tutor_mark
            progress.save()

    max_total_points = 0
    try:
        user_total_points = points_progress[str(lid)]
        statement_have_result = True
    except KeyError:
        statement_have_result = False
        user_total_points = 0

    for question in questions:
        max_total_points += question.points

    if profile.type_user == 'student':
        # check date access
        if check_date_access_to_course(progress):
            if statement_have_result:
                context = {
                    'lesson': lid_lesson,
                    'student': student,
                    'contents': contents,

                    'questions': questions,

                    'hw_images': hw_images,

                    'user_total_points': user_total_points,
                    'max_total_points': max_total_points,
                }
                return render(request, 'course/result_test_by_student.html', context)
            else:
                messages.warning(request, "Ви ще не виконали виконали домашню роботу. Сторінка не доступна!")
                return redirect('personal_cabinet')
        else:
            messages.warning(request, "На жаль, Ви не маєте доступу до цього курсу. Ви можете придбати підписку нижче!")
            cid = lesson.topic_fk.course_fk.id
            cid_course = get_object_or_404(Course, id=cid)
            context = {
                'course': cid_course,
                'topics': cid_course.topics.all(),
            }
            return render(request, 'course/false_access_data_view_course_student.html', context)
    elif profile.type_user == 'tutor' and statement_have_result:
        if progress.tutor_fk == request.user.profile.protutor:

            context = {
                'lesson': lid_lesson,
                'student': student,
                'contents': contents,

                'progress': progress,

                'questions': questions,

                'hw_images': hw_images,

                'user_total_points': user_total_points,
                'max_total_points': max_total_points,
            }
            return render(request, 'course/result_test_by_admin.html', context)
        else:
            messages.warning(request, "Ви не можете дивитись результати не призначених Вам Студентів!")
            return redirect('personal_cabinet')

    elif profile.type_user == 'head-teacher' and statement_have_result:
        if progress.tutor_fk in request.user.profile.proheadteacher.tutors:
            context = {
                'lesson': lid_lesson,
                'student': student,
                'contents': contents,

                'questions': questions,

                'progress': progress,

                'hw_images': hw_images,

                'user_total_points': user_total_points,
                'max_total_points': max_total_points,
            }
            return render(request, 'course/result_test_by_admin.html', context)
        else:
            messages.warning(request, "Ви не можете дивитись результати не призначених Вам Студентів!")
            return redirect('personal_cabinet')

    elif profile.type_user == 'parent' and statement_have_result:
        if student.parent_fk == profile.proparent:
            context = {
                'lesson': lid_lesson,
                'student': student,
                'contents': contents,

                'questions': questions,

                'hw_images': hw_images,

                'user_total_points': user_total_points,
                'max_total_points': max_total_points,
            }
            return render(request, 'course/result_test_by_admin.html', context)
        else:
            messages.warning(request, "Ви не можете дивитись результати не зареєстрованих Вами Студентів!")
    elif statement_have_result is False:
        messages.warning(request, "Студент ще не виконав домашнє завдання по цьому уроку!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, "Вибачте, сторінка, на яку Ви намагались потрапити, тимчасово недоступна!")
        return redirect('personal_cabinet')


def check_answers(lid, sid):
    statement = False
    lid_lesson = Lesson.objects.get(id=lid)
    sid_student = ProStudent.objects.get(id=sid)
    for question in lid_lesson.questions.all():
        answer = AnswerQuestion.objects.filter(question_fk=question, student_fk=sid_student)
        if len(answer) > 0:
            statement = True
            break
    return statement
