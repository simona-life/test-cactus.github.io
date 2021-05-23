from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from django.utils.datetime_safe import date
from django.http import HttpResponseRedirect

from django.shortcuts import (render,
                              redirect,
                              get_object_or_404)
from django.contrib.auth.decorators import login_required

from access.models import Progress
from account.models import (Profile,
                            ProTutor,
                            ProParent)
from course.models import Course
from private_lesson.models import PrivateLesson
from timetable.models import MonthTutorTimetable

from access.views import check_date_access_to_course

from access.decorators import (tutor_type_only,
                               parent_type_only,
                               student_type_only,
                               head_teacher_type_only)


@login_required
def private_lesson_view(request, lid):
    lid_lesson = PrivateLesson.objects.get(id=lid)
    cid = lid_lesson.progress_fk.id_course
    profile = Profile.objects.get(user=request.user)
    if lid_lesson.lesson_date < date.today():
        return HttpResponseRedirect(reverse('result_private_lesson_view', kwargs={'lid': lid}))
    else:
        if profile.type_user == 'student':
            return HttpResponseRedirect(reverse('private_lesson_view_by_student', kwargs={'lid': lid}))
        elif profile.type_user == 'tutor':
            return HttpResponseRedirect(reverse('private_lesson_view_by_tutor', kwargs={'lid': lid}))
        elif profile.type_user == 'head-teacher':
            return HttpResponseRedirect(reverse('private_lesson_view_by_head_teacher', kwargs={'lid': lid}))
        elif profile.type_user == 'parent':
            messages.info(request, "Цей урок ще не було проведено, тому результатів немає. Спробуйте пізніше!")
            return redirect('personal_cabinet')
        else:
            messages.warning(request, "На жаль, Ви не маєте доступу до цього курсу. Ви можете придбати підписку нижче!")
            return HttpResponseRedirect(reverse('course_details', kwargs={'cid': cid}))


@login_required
@student_type_only
def private_lesson_view_by_student(request, lid):
    lid_lesson = PrivateLesson.objects.get(id=lid)
    progress = lid_lesson.progress_fk
    cid = lid_lesson.progress_fk.id_course
    tutor = progress.tutor_fk

    action = request.POST.get('action')

    if request.POST and action == 'Відмінити урок':
        if lid_lesson.lesson_date > date.today():
            if progress.include_month_private_lessons_current < progress.include_month_private_lessons_include_default:
                progress.include_month_private_lessons_current += 1
                progress.save()
            elif progress.include_month_private_lessons_current == progress.include_month_private_lessons_include_default:
                progress.qty_bought_private_lessons += 1
                progress.save()
            messages.success(request, "Заняття з Тьютором було успішно відмінено.")
            return redirect('personal_cabinet')
        else:
            messages.warning(request, "Вибачте! Ви не можете відмінити заняття в день його проведення.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # check date access
    if check_date_access_to_course(progress):
        # check date lesson
        if lid_lesson.lesson_date < date.today():
            return HttpResponseRedirect(reverse('result_private_lesson_view', kwargs={'lid': lid}))
        else:
            context = {
                'tutor': tutor,
                'lesson': lid_lesson,
            }
            return render(request, 'private_lesson/private_lesson/view_lesson_student.html', context=context)
    else:
        messages.warning(request, "На жаль, Ви не маєте доступу до цього курсу. Ви можете придбати підписку нижче!")
        cid_course = get_object_or_404(Course, id=cid)
        context = {
            'course': cid_course,
            'topics': cid_course.topics.all(),
        }
        return render(request, 'course/false_access_data_view_course_student.html', context=context)


@login_required
@tutor_type_only
def private_lesson_view_by_tutor(request, lid):
    profile = Profile.objects.get(user=request.user)
    lid_lesson = PrivateLesson.objects.get(id=lid)
    tutor = ProTutor.objects.get(profile=profile)
    progress = lid_lesson.progress_fk
    student = lid_lesson.student_fk

    action = request.POST.get('action')

    if request.POST and action == 'Відмінити урок':
        if lid_lesson.lesson_date > date.today():
            if progress.include_month_private_lessons_current < progress.include_month_private_lessons_include_default:
                progress.include_month_private_lessons_current += 1
                progress.save()
            elif progress.include_month_private_lessons_current == progress.include_month_private_lessons_include_default:
                progress.qty_bought_private_lessons += 1
                progress.save()
            messages.success(request, "Заняття було успішно відмінено.")
            return redirect('personal_cabinet')
        else:
            messages.warning(request, "Вибачте! Ви не можете відмінити заняття в день його проведення.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if progress.tutor_fk == tutor:
        # check date lesson
        if lid_lesson.lesson_date < date.today():
            return HttpResponseRedirect(reverse('result_private_lesson_view', kwargs={'lid': lid}))
        else:
            context = {
                'student': student,
                'lesson': lid_lesson,
            }
            return render(request, 'private_lesson/private_lesson/view_lesson_tutor.html', context=context)
    else:
        messages.warning(request, "Ви не можете дивитись заплановані приватні уроки не призначених Вам Студентів!")
        return redirect('personal_cabinet')


@login_required
@head_teacher_type_only
def private_lesson_view_by_head_teacher(request, lid):
    profile = Profile.objects.get(user=request.user)
    lid_lesson = PrivateLesson.objects.get(id=lid)
    tutor = lid_lesson.tutor_fk
    student = lid_lesson.student_fk

    if tutor in profile.proheadteacher.tutors:
        context = {
            'tutor': tutor,
            'student': student,
            'lesson': lid_lesson,
        }
        return render(request, 'private_lesson/private_lesson/view_lesson_head_teacher.html', context=context)
    else:
        messages.warning(request, "Ви не можете дивитись заплановані приватні уроки не призначених Вам Студентів!")
        return redirect('personal_cabinet')


# RESULT
@login_required
def result_private_lesson_view(request, lid):
    profile = Profile.objects.get(user=request.user)
    lid_lesson = PrivateLesson.objects.get(id=lid)
    cid = lid_lesson.progress_fk.id_course

    if lid_lesson.lesson_date < date.today():
        if profile.type_user == 'student':
            return HttpResponseRedirect(reverse('result_private_lesson_view_by_student', kwargs={'lid': lid}))
        elif profile.type_user == 'tutor':
            return HttpResponseRedirect(reverse('result_private_lesson_view_by_tutor', kwargs={'lid': lid}))
        elif profile.type_user == 'head-teacher':
            return HttpResponseRedirect(reverse('result_private_lesson_view_by_head_teacher', kwargs={'lid': lid}))
        elif profile.type_user == 'parent':
            return HttpResponseRedirect(reverse('result_private_lesson_view_by_parent', kwargs={'lid': lid}))
        else:
            messages.warning(request, "На жаль, Ви не маєте доступу до цього курсу. Ви можете придбати підписку нижче!")
            return HttpResponseRedirect(reverse('course_details', kwargs={'cid': cid}))
    else:
        return HttpResponseRedirect(reverse('private_lesson_view', kwargs={'lid': lid}))


@login_required
@parent_type_only
def result_private_lesson_view_by_parent(request, lid, pid):
    progress = Progress.objects.get(id=pid)
    parent = ProParent.objects.get(profile=request.user.profile)
    lid_lesson = PrivateLesson.objects.get(id=lid)
    tutor = lid_lesson.tutor_fk
    if progress.student_fk.parent_fk == parent:
        context = {
            'tutor': tutor,
            'lesson': lid_lesson,
        }
        return render(request, 'private_lesson/result_private_lesson/result_view_lesson_parent.html', context=context)
    else:
        messages.warning(request, "Ви не можете дивитись результати приватного уроку не доданих Вами студентів!")
        return redirect('personal_cabinet')


@login_required
@student_type_only
def result_private_lesson_view_by_student(request, lid):
    lid_lesson = PrivateLesson.objects.get(id=lid)
    tutor = lid_lesson.tutor_fk
    progress = lid_lesson.progress_fk
    cid = lid_lesson.progress_fk.id_course

    action = request.POST.get('action')

    if request.POST and action == 'Урок не було проведено':
        if not (lid_lesson.video_lesson and lid_lesson.report_tutor):
            if date.today() > lid_lesson.lesson_date:
                #  email for head_teacher !!!
                messages.success(request, "Хм, ми перевіримо інформацію та зв'яжемося з Вами! Дякуємо!")
                return redirect('personal_cabinet')
            else:
                messages.success(request, "Так швидко?) Тьютор ще не встиг завантажити свій звіт по Вашому заняттю, "
                                          "спробуйте трохи пізніше!)")
                return redirect('personal_cabinet')
        else:
            if lid_lesson.checked_by_head_teacher:
                messages.success(request,
                                 "Хм, мабуть, Ви помилились. Хед-тічер вже перевірив наявність звіту та відео з "
                                 "заняття. Якщо ми щось випустили, будь ласка, зв'яжіться з Вашим Хед-тічером!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.success(request,
                                 "Не хвилюйтесь, Хед-тічер поки перевірив наявність звіту та відео з "
                                 "заняття. Спробуйте трохи пізніше, ми вже перевіряємо звіт!) ")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # check date access
    if check_date_access_to_course(progress):
        context = {
            'tutor': tutor,
            'lesson': lid_lesson,
        }
        return render(request, 'private_lesson/result_private_lesson/result_view_lesson_student.html', context=context)
    else:
        messages.warning(request, "На жаль, Ви не маєте доступу до цього курсу. Ви можете придбати підписку нижче!")
        cid_course = get_object_or_404(Course, id=cid)
        context = {
            'course': cid_course,
            'topics': cid_course.topics.all(),
        }
        return render(request, 'course/false_access_data_view_course_student.html', context=context)


@login_required
@tutor_type_only
def result_private_lesson_view_by_tutor(request, lid):
    profile = Profile.objects.get(user=request.user)
    lid_lesson = PrivateLesson.objects.get(id=lid)
    tutor = ProTutor.objects.get(profile=profile)
    progress = lid_lesson.progress_fk
    student = lid_lesson.student_fk

    action = request.POST.get('action')

    if request.POST and action == 'Зберегти звіт':
        for video in request.FILES.getlist('photo'):
            lid_lesson.video_lesson = video
        lid_lesson.report_tutor = request.POST['report_tutor']
        lid_lesson.save()
        messages.success(request, 'Ви успішно додали звіт!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if progress.tutor_fk == tutor:
        context = {
            'student': student,
            'lesson': lid_lesson,
        }
        return render(request, 'private_lesson/result_private_lesson/result_view_lesson_tutor.html', context=context)
    else:
        messages.warning(request, "Ви не можете дивитись результати приватного уроку не призначених Вам Студентів!")
        return redirect('personal_cabinet')


@login_required
@head_teacher_type_only
def result_private_lesson_view_by_head_teacher(request, lid):
    profile = Profile.objects.get(user=request.user)
    lid_lesson = PrivateLesson.objects.get(id=lid)
    tutor = lid_lesson.tutor_fk
    student = lid_lesson.student_fk
    progress = lid_lesson.progress_fk

    action = request.POST.get('action')

    if request.POST and action == 'Зарахувати звіт':
        lid_lesson.checked_by_head_teacher = True
        lid_lesson.save()

        current_year = datetime.today().year
        current_month = datetime.today().month

        progress.qty_finished_private_lessons += 1
        progress.save()

        month_tutor_timetable = MonthTutorTimetable.objects.get(tutor_fk=tutor, month=current_month, year=current_year)
        month_tutor_timetable.qty_done_private_lessons += 1
        month_tutor_timetable.save()
        messages.success(request, 'Ви успішно перевірили та зарахували звіт!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if tutor in profile.proheadteacher.tutors:
        context = {
            'tutor': tutor,
            'student': student,
            'lesson': lid_lesson,
        }
        return render(request, 'private_lesson/result_private_lesson/result_view_lesson_head_teacher.html', context=context)
    else:
        messages.warning(request, "Ви не можете дивитись результати приватного уроку не призначених Вам Студентів!")
        return redirect('personal_cabinet')


@login_required
@parent_type_only
def result_private_lesson_view_by_parent(request, lid):
    profile = Profile.objects.get(user=request.user)
    lid_lesson = PrivateLesson.objects.get(id=lid)
    parent = ProParent.objects.get(profile=profile)
    progress = lid_lesson.progress_fk
    tutor = lid_lesson.tutor_fk
    student = lid_lesson.student_fk

    if progress.prostudent.tutor_fk == parent:
        context = {
            'tutor': tutor,
            'student': student,
            'lesson': lid_lesson,
        }
        return render(request, 'private_lesson/result_private_lesson/result_private_lesson_view_by_parent.html', context=context)
    else:
        messages.warning(request, "Ви не можете дивитись результати приватного уроку не доданих Вами студентів!")
        return redirect('personal_cabinet')


@login_required
@student_type_only
def all_private_lessons_in_course(request, cid):
    student = request.user.profile.prostudent
    progress = Progress.objects.get(student_fk=student, id_course=cid)
    all_lessons = PrivateLesson.objects.filter(progress_fk=progress)
    context = {
        "all_lessons": all_lessons,
    }
    return render(request, 'private_lesson/all_private_lessons_in_course.html', context=context)


@login_required
@tutor_type_only
def all_private_lessons_in_course_by_tutor(request):
    profile = Profile.objects.get(user=request.user)
    tutor = ProTutor.objects.get(profile=profile)
    all_lessons = PrivateLesson.objects.filter(tutor_fk=tutor)
    today_date = date.today()
    context = {
        "all_lessons": all_lessons,
        'today_date': today_date,
    }
    return render(request, 'private_lesson/all_private_lessons_in_course_by_tutor.html', context=context)


@login_required
@parent_type_only
def all_private_lessons_in_course_by_parent(request, pid):
    progress = Progress.objects.get(id=pid)
    parent = ProParent.objects.get(profile=request.user.profile)

    if progress.student_fk.parent_fk == parent:
        all_lessons = PrivateLesson.objects.filter(student_fk=progress.student_fk)
        today_date = date.today()
        context = {
            "all_lessons": all_lessons,
            'today_date': today_date,
        }
        return render(request, 'private_lesson/all_private_lessons_in_course_by_parent.html', context=context)
    else:
        messages.warning(request, "Ви не можете дивитись результати приватного уроку не доданих Вами студентів!")
        return redirect('personal_cabinet')
