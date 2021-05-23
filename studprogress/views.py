import json
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from access.views import get_tutor
from course.models import Course
from access.models import Progress
from account.models import (Profile,
                            ProTutor,
                            ProParent,
                            ProStudent,
                            ProHeadTeacher)

from access.decorators import (parent_type_only,
                               tutor_type_only,
                               head_teacher_type_only)


@login_required
@tutor_type_only
def student_progress_by_tutor(request, cid, sid):
    profile = Profile.objects.get(user=request.user)
    tutor = ProTutor.objects.get(profile=profile)
    student = ProStudent.objects.get(id=sid)

    action = request.POST.get('action')
    if request.POST:
        if action == 'Закрити доступ':
            progress = Progress.objects.get(student_fk=student, tutor_fk=tutor, id_course=cid)
            lessons_opened = json.loads(progress.lessons_opened)
            id_lesson = request.POST['lesson']
            lessons_opened[id_lesson] = False
            progress.lessons_opened = json.dumps(lessons_opened)
            progress.save()
            messages.success(request, f'Доступ до уроку з ID-{id_lesson} було успішно заборонено.')
        if action == 'Відкрити доступ':
            progress = Progress.objects.get(student_fk=student, tutor_fk=tutor, id_course=cid)
            lessons_opened = json.loads(progress.lessons_opened)
            id_lesson = request.POST['lesson']
            lessons_opened[id_lesson] = True
            progress.lessons_opened = json.dumps(lessons_opened)
            progress.save()
            messages.success(request, f'Доступ до уроку з ID-{id_lesson} було успішно дозволено.')

    try:
        progress = Progress.objects.get(student_fk=student, tutor_fk=tutor, id_course=cid)
    except Progress.DoesNotExist:
        messages.warning(request, "Ви не є Тьютором даного Студента! Будь ласка, скористайтесь особистим кабінетом "
                                  "для відображення своїх студентів")
        return redirect('personal_cabinet')

    course = Course.objects.get(id=cid)
    context = {
        'course': course,
        'student': student,
        'progress': progress,
    }
    return render(request, 'studprogress/student_progress_by_tutor.html', context=context)


@login_required
@head_teacher_type_only
def student_progress_by_head_teacher(request, cid, sid):
    action = request.POST.get('action')
    if request.POST:
        student = ProStudent.objects.get(id=sid)
        progress = Progress.objects.get(student_fk=student, id_course=cid)
        if action == 'Закрити доступ':
            lessons_opened = json.loads(progress.lessons_opened)
            id_lesson = request.POST['lesson']
            lessons_opened[id_lesson] = False
            progress.lessons_opened = json.dumps(lessons_opened)
            progress.save()
            messages.success(request, f'Доступ до уроку з ID {id_lesson} було успішно заборонено.')
            return redirect('student_progress_by_head_teacher', args=(cid, sid))
        if action == 'Відкрити доступ':
            lessons_opened = json.loads(progress.lessons_opened)
            id_lesson = request.POST['lesson']
            lessons_opened[id_lesson] = True
            progress.lessons_opened = json.dumps(lessons_opened)
            progress.save()
            messages.success(request, f'Доступ до уроку з ID {id_lesson} було успішно дозволено.')
            return redirect('student_progress_by_head_teacher', args=(cid, sid))
        if action == 'Призначити Тьютора':
            new_tutor = request.POST['tutor']
            progress.tutor_fk = new_tutor
            progress.save()
            messages.success(request, "Чудово! Тьютор був успішно призначений!")
            return redirect('student_progress_by_head_teacher', args=(cid, sid))
        if action == 'Призначити іншого Тьютора':
            progress.tutor_fk.delete()
            progress.save()
            messages.success(request, "Тьютор був успішно видалений з замовлення. Оберіть нового Тьютора!")
            return redirect('student_progress_by_head_teacher', args=(cid, sid))
        if action == 'Призначити іншого Тьютора системою':
            got = get_tutor(cid, progress)
            if got:
                messages.success(request, "Тьютор був успішно призначений. Дякуємо!")
                return redirect('head_teacher_personal_cabinet')
            else:
                messages.info(request, 'На жаль поки немає вільних Тьюторів для даного Курсу.')
                return redirect('student_progress_by_head_teacher', args=(cid, sid))

    profile = Profile.objects.get(user=request.user)
    head_teacher = ProHeadTeacher.objects.get(profile=profile)

    id_courses = []
    for course in head_teacher.courses.all():
        id_courses.append(int(course.id))

    if int(cid) in id_courses:
        all_hd_tutors = head_teacher.tutors.all()
        course = Course.objects.get(id=cid)
        student = ProStudent.objects.get(id=sid)
        progress = Progress.objects.get(student_fk=student, id_course=cid)
        tutor = progress.tutor_fk

        tutors = ProTutor.objects.filter(head_teacher_fk=head_teacher, courses=course)

        if progress.tutor_fk is None or progress.tutor_fk.head_teacher_fk == head_teacher:
            context = {
                'head_teacher': head_teacher,
                'all_hd_tutors': all_hd_tutors,
                'course': course,
                'student': student,
                'progress': progress,
                'tutor': tutor,
                'tutors': tutors,
            }
            return render(request, 'studprogress/student_progress_by_head_teacher.html', context=context)
        else:
            messages.warning(request, "Цей студент вже має Тьютора! Будь ласка, скористайтесь особистим кабінетом "
                                      "для відображення Ваших Студентів та Тьюторів.")
            return redirect('personal_cabinet')
    else:
        messages.warning(request, "Ви не є Хед-тічером даного курса! Будь ласка, скористайтесь особистим кабінетом "
                                  "для відображення призначених Вам курсів.")
        return redirect('personal_cabinet')


@login_required
@parent_type_only
def student_progress_by_parent(request, cid, sid):
    student = ProStudent.objects.get(id=sid)
    profile = Profile.objects.get(user=request.user)
    parent = ProParent.objects.get(profile=profile)
    if student.parent_fk == parent:
        course = Course.objects.get(id=cid)
        student = ProStudent.objects.get(id=sid)
        progress = Progress.objects.get(student_fk=student, id_course=cid)
        context = {
            'course': course,
            'student': student,
            'progress': progress,
        }
        return render(request, 'studprogress/student_progress_by_parent.html', context=context)
    else:
        messages.warning(request, "Ви не є Батьками даного Студента! Будь ласка, скористайтесь особистим кабінетом "
                                  "для відображення Ваших Студентів.")
        return redirect('personal_cabinet')
