import json
import random
import string

from django.contrib import messages
from django.shortcuts import (render,
                              redirect,
                              get_object_or_404)

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.utils.datetime_safe import date


from dateutil.relativedelta import relativedelta

from course.models import Course
from access.models import (Progress)
from account.models import (Profile,
                            ProStudent,
                            ProParent)

from access.forms import (ParentFormFirstBuy,
                          StudentFormFirstBuy)

from access.decorators import (guest_type_only,
                               parent_type_only,
                               student_type_only,
                               login_required_message)


@login_required_message(message='Для того, щоб купити курс потрібно увійти у акаунт!')
@login_required(redirect_field_name='next')
def buy_course(request, cid):
    profile = Profile.objects.get(user=request.user)
    if profile.type_user == 'guest':
        return redirect('buy_course_by_guest', cid)
    elif profile.type_user == 'parent':
        parent = ProParent.objects.get(profile=profile)
        if parent.students.exists():
            return redirect('buy_course_by_parent', cid)
        else:
            parent.delete()
            profile.type_user = 'guest'
            return redirect('buy_course_by_guest', cid)
    elif profile.type_user == 'student':
        return redirect('buy_course_by_student', cid)
    elif profile.type_user == 'head-teacher' or profile.type_user == 'tutor':
        # message
        messages.info(request, 'Для Тьюторів та Хед-тічерів функція покупки курсу поки не доступна')
        return redirect('all_courses')


# if Parent has more than 1 Student
@login_required_message(message='Для того, щоб купити курс потрібно увійти у акаунт!')
@login_required
@parent_type_only
def buy_course_by_parent(request, cid):
    cid_course = get_object_or_404(Course, id=cid)
    parent_profile = Profile.objects.get(user=request.user)
    parent = ProParent.objects.get(profile=parent_profile)
    students = parent.students.all()
    profile = Profile.objects.get(user=request.user)

    if len(students) == 0:
        parent.delete()
        profile.type_user = 'guest'
        profile.save()
        messages.info(request, 'У Вас не було жодного доданого студента, можливо вони видалили свої профілі. Тому Вам '
                               'надано статус Гість!')
        return redirect('buy_course', cid)
    elif len(students) == 1:
        sid = students[0].id
        return redirect('buy_course_by_parent_student', cid, sid)
    else:
        context = {
            'course': cid_course,
            'students': students,
        }
        return render(request, 'buy_course/buy_course_by_parent_students.html', context)


# if Parent has 1 Student
@login_required_message(message='Для того, щоб купити курс потрібно увійти у акаунт!')
@login_required
@parent_type_only
def buy_course_by_parent_student(request, cid, sid):
    action = request.POST.get('action')
    cid_course = Course.objects.get(id=cid)
    student = get_object_or_404(ProStudent, id=sid)

    if request.POST:
        if action == 'Оплатити (успіх)':  # success buying logic
            months = request.POST['type_sub']
            if Progress.objects.filter(id_course=cid, student_fk=student).exists():
                current_progress = Progress.objects.get(id_course=cid, student_fk=student)
                continue_date_access_to_course(months, current_progress, cid_course)  # with private lessons adding!
            else:
                lessons_opened = first_open_lessons_in_course(cid)
                current_progress = first_create_progress(student, lessons_opened, cid)  # with private lessons adding!
                get_tutor(cid, current_progress)
                date_access_to_course(months, current_progress, cid_course)
            # message
            messages.warning(request, f'Вітаємо! Ви успішно оплатили навчання! Кількість місяців: {months}')
            return redirect('all_courses')
        if action == 'Оплатити (поразка)':  # lose buying logic
            # message
            messages.warning(request, 'Щось пішло не так, спробуйте ще раз!')

    context = {
        'course': cid_course,
        'student': student,
    }
    return render(request, 'buy_course/buy_course_by_parent_student.html', context)


@login_required_message(message='Для того, щоб купити курс потрібно увійти у акаунт!')
@login_required
@student_type_only
def buy_course_by_student(request, cid):
    action = request.POST.get('action')
    profile = request.user.profile
    student = get_object_or_404(ProStudent, profile=profile)

    if request.POST:
        if action == 'Оплатити (успіх)':  # success buying logic
            months = request.POST['type_sub']
            if Progress.objects.filter(id_course=cid, student_fk=student).exists():
                current_progress = Progress.objects.get(id_course=cid, student_fk=student)
                cid_course = Course.objects.get(id=cid)
                continue_date_access_to_course(months, current_progress, cid_course)
            else:
                cid_course = Course.objects.get(id=cid)
                lessons_opened = first_open_lessons_in_course(cid)
                current_progress = first_create_progress(student, lessons_opened, cid)
                get_tutor(cid, current_progress)
                date_access_to_course(months, current_progress, cid_course)

            # message
            messages.warning(request, f'Вітаємо! Ви успішно оплатили навчання! Кількість місяців: {months}')
            return redirect('all_courses')
        if action == 'Оплатити (поразка)':  # lose buying logic
            # message
            messages.warning(request, 'Щось пішло не так, спробуйте ще раз!')

    cid_course = Course.objects.get(id=cid)
    context = {
        'course': cid_course,
    }
    return render(request, 'buy_course/buy_course_by_student.html', context)


@login_required_message(message='Для того, щоб купити курс потрібно увійти у акаунт!')
@login_required
@guest_type_only
def buy_course_by_guest(request, cid):
    cid_course = get_object_or_404(Course, id=cid)
    profile = Profile.objects.get(user=request.user)

    parent_form = ParentFormFirstBuy()
    student_form = StudentFormFirstBuy()

    action = request.POST.get('action')

    if request.POST:
        if action == 'Оплатити (успіх)':  # success buying logic
            # success logic
            months = request.POST['type_sub']
            # parent buys course
            if 'first_name_student' in request.POST:
                parent_form = ParentFormFirstBuy(request.POST)
                if parent_form.is_valid():
                    # get date from form
                    first_name_student = request.POST['first_name_student']
                    last_name_student = request.POST['last_name_student']
                    email_student = request.POST['email_student']
                    phone_number_student = request.POST['phone_number_student']
                    current_progress = guest_parent_first_buy(cid,
                                                              profile,
                                                              first_name_student,
                                                              last_name_student,
                                                              email_student,
                                                              phone_number_student)
                    date_access_to_course(months, current_progress, cid_course)
                else:
                    # message
                    messages.warning(request, 'Користувач з таким номером телефону або e-mail вже існує! Будь ласка, '
                                              'перевірте правильність Ваших даних!')
                    # return with POST form
                    parent_form = ParentFormFirstBuy(request.POST)
                    student_form = StudentFormFirstBuy()
                    context = {
                        'course': cid_course,
                        'parent_form': parent_form,
                        'student_form': student_form,
                    }
                    return render(request, 'buy_course/buy_course_by_guest.html', context)
            # student buys course
            else:
                current_progress = guest_student_first_buy(cid, profile)
                date_access_to_course(months, current_progress, cid_course)
            # message
            messages.success(request, f'Вітаємо! Ви успішно оплатили навчання! Кількість місяців: {months}')
            return redirect('all_courses')
        if action == 'Оплатити (поразка)':  # lose buying logic
            # lose logic

            # message
            messages.warning(request, 'Щось пішло не так, спробуйте ще раз!')
            # return with POST forms
            parent_form = ParentFormFirstBuy(request.POST)
            student_form = StudentFormFirstBuy(request.POST)
            context = {
                'course': cid_course,
                'parent_form': parent_form,
                'student_form': student_form,
            }
            return render(request, 'buy_course/buy_course_by_guest.html', context=context)

    context = {
        'course': cid_course,
        'parent_form': parent_form,
        'student_form': student_form,
    }
    return render(request, 'buy_course/buy_course_by_guest.html', context)


@login_required
@parent_type_only
def buy_additional_private_lessons_by_parent(request, cid, sid):
    profile = Profile.objects.get(user=request.user)
    parent = ProParent.objects.get(profile=profile)
    course = Course.objects.get(id=cid)

    action = request.POST.get('action')

    if request.POST:
        student = ProStudent.objects.get(id=sid)
        progress = Progress.objects.get(id_course=cid, student_fk=student)

        if action == 'Оплатити (успіх)':  # success buying logic
            # success logic
            count_private_lessons = request.POST['count_lessons']
            # summary_price = count_private_lessons * course.price_private_lesson
            progress.qty_bought_private_lessons += count_private_lessons
            progress.save()
            messages.success(request, f'Вітаємо! Ви успішно оплатили навчання! Кількість придбаних індивідуальних '
                                      f'уроків: {count_private_lessons}')
            return redirect('all_courses')

        if action == 'Оплатити (поразка)':  # lose buying logic
            # lose logic

            # message
            messages.warning(request, 'Щось пішло не так, спробуйте ще раз!')

            # return with POST forms
            context = {
                'progress': progress,
                'student': student,
                'course': course,
            }
            return render(request, 'buy_additional_private_lessons/buy_additional_private_lessons_by_parent.html',
                          context=context)

    # GET method
    if parent.students.exists():
        student = ProStudent.objects.get(id=sid)
        if student.parent_fk == parent:
            progress = Progress.objects.get(id_course=cid, student_fk=student)
            context = {
                'progress': progress,
                'student': student,
                'course': course,
            }
            return render(request, 'buy_additional_private_lessons/buy_additional_private_lessons_by_parent.html',
                          context=context)
        else:
            messages.warning(request, "Ви не можете придбати персональний урок не доданими Вами Студентами.")
            return redirect('personal_cabinet')
    else:
        parent.delete()
        profile.type_user = 'guest'
        profile.save()
        messages.info(request, "У Вас не було жодного Студента, тому Вам присвоєний статус Гість")
        return redirect('all_courses')


@login_required
@student_type_only
def buy_additional_private_lessons_by_student(request, cid):
    profile = Profile.objects.get(user=request.user)
    course = Course.objects.get(id=cid)
    student = ProStudent.objects.get(profile=profile)
    progress = Progress.objects.get(id_course=cid, student_fk=student)

    action = request.POST.get('action')

    if request.POST:

        if action == 'Оплатити (успіх)':  # success buying logic
            # success logic
            count_private_lessons = request.POST['count_lessons']
            # summary_price = count_private_lessons * course.price_private_lesson
            progress.qty_bought_private_lessons += count_private_lessons
            progress.save()
            messages.success(request, f'Вітаємо! Ви успішно оплатили навчання! Кількість придбаних індивідуальних '
                                      f'уроків: {count_private_lessons}')
            return redirect('all_courses')

        if action == 'Оплатити (поразка)':  # lose buying logic
            # lose logic

            # message
            messages.warning(request, 'Щось пішло не так, спробуйте ще раз!')

            # return with POST forms
            context = {
                'progress': progress,
                'student': student,
                'course': course,
            }
            return render(request, 'buy_additional_private_lessons/buy_additional_private_lessons_by_student.html',
                          context=context)

    # GET method
    context = {
        'progress': progress,
        'student': student,
        'course': course,
    }
    return render(request, 'buy_additional_private_lessons/buy_additional_private_lessons_by_student.html',
                  context=context)


# returns PROGRESS
def guest_parent_first_buy(cid,
                           profile,
                           first_name_student,
                           last_name_student,
                           email_student,
                           phone_number_student):
    # update type_user to parent, create ProParent
    profile.type_user = 'parent'
    profile.save()
    pro_parent = ProParent.objects.create(profile=profile)
    pro_parent.save()
    # generate random username and password
    username = create_username()
    password = create_password()
    # create student
    student_user = User.objects.create_user(username=username,
                                            first_name=first_name_student,
                                            last_name=last_name_student,
                                            email=email_student)
    student_user.set_password(password)
    student_user.save()
    student_profile = Profile.objects.create(user=student_user,
                                             phone_number=phone_number_student,
                                             type_user='student')
    student_profile.save()
    pro_student = ProStudent.objects.create(profile=student_profile,
                                            parent_fk=pro_parent)
    # email for new_student


    # мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!мейл!
    # open first lesson, create progress, get tutor
    lessons_opened = first_open_lessons_in_course(cid)
    current_progress = first_create_progress(pro_student, lessons_opened, cid)
    get_tutor(cid, current_progress)
    return current_progress


# returns PROGRESS
def guest_student_first_buy(cid, profile):
    # update type_user to student, create ProStudent
    profile.type_user = 'student'
    profile.save()
    pro_student = ProStudent.objects.create(profile=profile)
    # open first lesson, create progress, get tutor
    lessons_opened = first_open_lessons_in_course(cid)
    current_progress = first_create_progress(pro_student, lessons_opened, cid)
    get_tutor(cid, current_progress)
    return current_progress


# for rebuy and buy course
def date_access_to_course(months, current_progress, cid_course):
    try:
        months = int(months)
        today = date.today()
        rebuy_date = today + relativedelta(months=+months)
        current_progress.start_sub_date = today
        current_progress.end_sub_date = rebuy_date
        current_progress.include_month_private_lessons_current = months * current_progress.include_month_private_lessons_include_default
        current_progress.save()
        return True
    except:
        print('Some problem in date_access_to_course')
        #  mail ?
        return False


# for continue access course AND adding new private lessons
def continue_date_access_to_course(months, current_progress, cid_course):
    try:
        months = int(months)
        end_date = current_progress.end_sub_date
        rebuy_date = end_date + relativedelta(months=+months)
        current_progress.end_sub_date = rebuy_date
        current_progress.include_month_private_lessons_current += months * current_progress.include_month_private_lessons_include_default
        current_progress.save()
        return True
    except:
        print('Some problem in continue_date_access_to_course')
        #  mail ?
        return False


# returns True or False
def check_date_access_to_course(current_progress):
    if current_progress.end_sub_date > date.today():
        current_progress.is_active = False
        current_progress.save()
        return True
    else:
        current_progress.is_active = False
        current_progress.save()
        return False


# returns True or False
def get_tutor(cid, current_progress):
    current_course = Course.objects.get(id=cid)
    tutors = current_course.tutors
    try:
        for tutor in tutors:
            current_qty_students = tutor.students_progresses.all()
            if len(current_qty_students) < tutor.chose_qty_students:
                current_progress.tutor_fk = tutor
                current_progress.save()
                return True
    except TypeError:
        print('Fuck(( Any tutors')
        # mail??
        return False


# returns JSON lessons_opened
def first_open_lessons_in_course(course_id):
    bought_course = Course.objects.get(id=course_id)
    first_topic = bought_course.topics.get(order=1)
    first_lesson = first_topic.lessons.get(order=1)
    lessons_opened = {}
    for topic in bought_course.topics.all():
        for current_lesson in topic.lessons.all():
            lessons_opened[str(current_lesson.id)] = False
    lessons_opened[str(first_lesson.id)] = True
    lessons_opened = json.dumps(lessons_opened)
    return lessons_opened


# returns PROGRESS
def first_create_progress(new_pro_student, lessons_opened, course_id):
    cid_course = Course.objects.get(id=course_id)
    include_month_private_lessons_default = cid_course.include_month_private_lessons_default
    current_progress = Progress.objects.create(student_fk=new_pro_student,
                                               lessons_opened=lessons_opened,
                                               id_course=course_id)
    current_progress.include_month_private_lessons_include_default = include_month_private_lessons_default
    current_progress.include_month_private_lessons_current = include_month_private_lessons_default
    current_progress.save()
    return current_progress


# returns USERNAME
def create_username():
    def try_create():
        username_in = 'user'
        for _ in range(5):
            username_in += str(random.randint(1, 9))
        return username_in

    while True:
        username = try_create()
        if User.objects.filter(username=username).exists():
            pass
        else:
            break
    return username


# returns PASSWORD
def create_password():
    password = ''
    i = 1
    while i < 13:
        choice = random.randint(1, 2)
        if choice == 1:
            password += random.choice(string.ascii_letters)
        else:
            password += str(random.randint(0, 9))
        i += 1
    return password


# returns True or False
def check_open_lesson(progress, lid):
    lessons_open_dict = json.loads(progress.lessons_opened)
    if str(lid) in lessons_open_dict:
        return True
    else:
        return False
