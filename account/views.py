import json
import calendar

from datetime import datetime

from django.contrib.auth.views import redirect_to_login
from django.utils.datetime_safe import date

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from access.views import get_tutor
from account.forms import (UserEditForm,
                           ProfileEditForm,
                           UserRegisterForm,
                           ProfileRegisterForm)

from access.my_captcha import FormWithCaptcha

from course.models import Course
from access.models import Progress
from account.models import (Profile,
                            ProTutor,
                            ProParent,
                            ProStudent,
                            ProHeadTeacher)
from private_lesson.models import PrivateLesson

from access.decorators import (tutor_type_only,
                               guest_type_only,
                               parent_type_only,
                               student_type_only,
                               head_teacher_type_only,
                               login_required_message)
from timetable.models import MonthTutorTimetable
from send_emails.views import (email_for_new_tutor,
                               get_admins_emails_list,
                               dismiss_email_for_tutor,
                               new_tutor_by_headteacher_for_admin_mail)


@login_required
def personal_cabinet(request):
    profile = Profile.objects.get(user=request.user)
    if profile.type_user == 'student':
        return redirect('student_personal_cabinet')
    elif profile.type_user == 'parent':
        return redirect('parent_personal_cabinet')
    elif profile.type_user == 'tutor':
        return redirect('tutor_personal_cabinet')
    elif profile.type_user == 'guest':
        return redirect('all_courses')
    elif profile.type_user == 'head-teacher':
        return redirect('head_teacher_personal_cabinet')
    else:
        messages.warning(request, "На жаль, Ви не можете потрапити на цю сторінку.")
        return render(request, 'course/all_courses_user.html')


@login_required(redirect_field_name='next')
@student_type_only
def student_personal_cabinet(request):
    progresses = Progress.objects.filter(student_fk=request.user.profile.prostudent)
    if len(progresses) == 0:
        progresses = 0
    context = {
        'progresses': progresses,
    }
    return render(request, 'cabinets/student_cabinet.html', context=context)


@login_required(redirect_field_name='next')
@parent_type_only
def parent_personal_cabinet(request):
    parent = ProParent.objects.get(profile=request.user.profile)
    students = parent.students.all()
    profile = Profile.objects.get(user=request.user)

    if len(students) == 0:
        parent.delete()
        profile.type_user = 'guest'
        messages.info(request, 'У Вас не було жодного доданого студента, можливо вони видалили свої профілі. Тому Вам '
                               'надано статус Гість!')
        return redirect('all_courses')

    # parent has 1 student
    elif len(students) == 1:
        student = students[0]
        return redirect('sid_student_info_for_parent', sid=student.id)
    else:
        return redirect('parents_students_view')


# parent has more than 1 students
@login_required(redirect_field_name='next')
@parent_type_only
def parents_students_view(request):
    parent = ProParent.objects.get(profile=request.user.profile)
    students = parent.students.all()
    context = {
        'students': students,
    }
    return render(request, 'cabinets/parents_students.html', context=context)


@login_required(redirect_field_name='next')
@parent_type_only
def sid_student_info_for_parent(request, sid):
    student = ProStudent.objects.get(id=sid)

    context = {
        'student': student,
    }
    return render(request, 'cabinets/sid_parents_student.html', context=context)


@login_required(redirect_field_name='next')
@tutor_type_only
def tutor_personal_cabinet(request):
    profile = Profile.objects.get(user=request.user)
    tutor = ProTutor.objects.get(profile=profile)
    tutors_students_progresses = tutor.students_progresses.all()
    current_qty_students = len(tutors_students_progresses)

    current_year = datetime.today().year
    current_month = datetime.today().month

    today_day = date.today().day
    today_weekday = date.today().weekday()

    max_day_month = calendar.monthrange(current_year, current_month)[1]

    # лучше сделать фильтрацию по 7 дням этой недели
    private_lessons = PrivateLesson.objects.filter(tutor_fk=tutor)

    try:
        def_obj = MonthTutorTimetable.objects.get(tutor_fk=tutor, month=current_month, year=current_year)
        selected_weekdays = json.loads(def_obj.selected_weekdays)
        booked_weekdays = json.loads(def_obj.booked_weekdays)

    except MonthTutorTimetable.DoesNotExist:
        selected_weekdays = {}
        booked_weekdays = {}

    all_lessons = PrivateLesson.objects.filter(tutor_fk=tutor)
    today_date = date.today()

    context = {
        'user': request.user,
        'profile': profile,
        'tutor': tutor,
        'tutors_students_progresses': tutors_students_progresses,
        'current_qty_students': current_qty_students,

        'private_lessons': private_lessons,

        'selected_weekdays': selected_weekdays,
        'booked_weekdays': booked_weekdays,

        'max_day_month': max_day_month,
        'today_day': today_day,
        'today_weekday': today_weekday,
        'current_month': current_month,

        'all_lessons': all_lessons,
        'today_date': today_date,
    }
    return render(request, 'cabinets/tutor_cabinet.html', context=context)


@login_required(redirect_field_name='next')
@head_teacher_type_only
def head_teacher_personal_cabinet(request):
    profile = Profile.objects.get(user=request.user)
    head_teacher = ProHeadTeacher.objects.get(profile=profile)

    action = request.POST.get('action')
    if request.POST and action == 'Додати тьютора':
        tutor_email = request.POST['email']
        try:
            tutor_user = User.objects.get(email=tutor_email)
            tutor_profile = tutor_user.profile
            tutor_course = request.POST['course']
            if tutor_profile.type_user == 'guest':
                tutor_profile.type_user = 'tutor'
                tutor_profile.save()
                tutor = ProTutor.objects.create(profile=tutor_profile, courses=tutor_course, head_teacher_fk=head_teacher)

                #  mail for new tutor
                email_for_new_tutor(head_teacher.id, tutor.id, tutor_course.id, tutor_email)

                #  mail for admin/admins
                for admin_mail in get_admins_emails_list():
                    new_tutor_by_headteacher_for_admin_mail(head_teacher.id, tutor.id, tutor_course.id, admin_mail)

            else:
                messages.warning(request, "Цей юзер має іншу роль на сайті, дія неможлива!")
        except User.DoesNotExist:
            messages.warning(request,
                             "Юзера з таким email не існує! Будь ласка, перевірте правильність введених даних!")

    head_teacher = ProHeadTeacher.objects.get(profile=profile)
    tutors = head_teacher.tutors.all()
    qty_tutors = len(tutors)

    if len(tutors) == 0:
        tutors = 0

    courses_ids = []
    for course in head_teacher.courses.all():
        courses_ids.append(int(course.id))
    without_tutor_students_progresses = Progress.objects.filter(tutor_fk=None, id_course__in=courses_ids)

    all_hd_courses = Course.objects.filter(id__in=courses_ids)

    context = {
        'user': request.user,
        'profile': profile,
        'head_teacher': head_teacher,
        'courses': all_hd_courses,
        'tutors': tutors,
        'qty_tutors': qty_tutors,
        'without_tutor_students_progresses': without_tutor_students_progresses,
    }
    return render(request, 'cabinets/head_teacher_cabinet.html', context=context)


@login_required(redirect_field_name='next')
@head_teacher_type_only
def tutor_info(request, tid):
    tutor_profile = Profile.objects.get(id=tid)
    tutor = ProTutor.objects.get(profile=tutor_profile)
    tutors_students_progresses = tutor.students_progresses.all()
    current_qty_students = len(tutors_students_progresses)

    action = request.POST.get('action')
    if request.POST and action == 'Звільнити Тьютора':
        # mail for tutor
        dismiss_email_for_tutor(tutor.id, tutor_profile.user.email)

        # mail for headteacher

        # mail for admin/admins

        if len(tutors_students_progresses) == 0:
            tutor_profile.type_user = 'guest'
            tutor.delete()
        else:
            for students_progress in tutors_students_progresses:
                # try to get new tutor for each student
                cid = students_progress.id_course
                students_progress.tutor_fk.delete()
                statement = get_tutor(cid, students_progress)

                if not statement:
                    # mail for headteachers
                    pass

            tutor_profile.type_user = 'guest'
            tutor.delete()
        messages.success(request, 'Ви успішно звільнили Тьютора!')

    private_lessons_checked = PrivateLesson.objects.filter(tutor_fk=tutor, checked_by_head_teacher=True)
    if len(private_lessons_checked) == 0:
        private_lessons_checked = 0
    private_lessons_unchecked = PrivateLesson.objects.filter(tutor_fk=tutor, checked_by_head_teacher=False)
    if len(private_lessons_unchecked) == 0:
        private_lessons_unchecked = 0

    context = {
        'user': request.user,
        'profile': tutor_profile,
        'tutor': tutor,
        'tutors_students_progresses': tutors_students_progresses,
        'current_qty_students': current_qty_students,
        'private_lessons_checked': private_lessons_checked,
        'private_lessons_unchecked': private_lessons_unchecked,
    }
    return render(request, 'tutor_info.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваші дані було успішно змінено!')
        return redirect('personal_cabinet')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/edit.html',
                      {'user_form': user_form, 'profile_form': profile_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
        captcha_form = FormWithCaptcha(request.POST)
        if user_form.is_valid() and profile_form.is_valid() and captcha_form.is_valid():
            # create new user, but do not save to db
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            # save user in db.
            new_user.save()
            # creation profile
            new_profile = Profile.objects.create(user=new_user)
            # add type_user, phone number in Profile
            edit_profile = Profile.objects.get(user=new_user)
            edit_profile.phone_number = request.POST.get('phone_number')
            edit_profile.type_user = 'guest'
            edit_profile.save()
            # message
            messages.success(request, 'Чудово! Тепер Ви маєте свій обліковий запис!')
            if 'next_url' in request.session:
                return redirect_to_login(request.session['next_url'])
            else:
                return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
        captcha_form = FormWithCaptcha()
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'captcha_form': captcha_form,
    }
    return render(request, 'account/register.html', context=context)


def getListWeekdayTimes(week_day, default_hours_dict):
    default_hours_id_list = []
    ID_DICT = {'8:00-9:00': 1,
               '9:00-10:00': 2,
               '10:00-11:00': 3,
               '11:00-12:00': 4,
               '12:00-13:00': 5,
               '13:00-14:00': 6,
               '14:00-15:00': 7,
               '15:00-16:00': 8,
               '16:00-17:00': 9,
               '17:00-18:00': 10,
               '18:00-19:00': 11,
               '19:00-20:00': 12,
               '20:00-21:00': 13,
               }

    ID_DAYS = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }
