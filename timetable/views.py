import json
import calendar

from datetime import datetime
from django.utils.datetime_safe import date

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from access.models import Progress
from access.views import check_date_access_to_course
from account.models import (Profile,
                            ProTutor,
                            ProHeadTeacher)
from course.models import Course
from private_lesson.models import PrivateLesson

from timetable.models import (MonthTutorTimetable,
                              MonthStudentTimetable,
                              SelectedWorkingHoursByDefault)

from access.decorators import (tutor_type_only,
                               guest_type_only,
                               parent_type_only,
                               student_type_only,
                               head_teacher_type_only,
                               login_required_message)

NAMES_MONTHS = {
    1: 'Січень',
    2: 'Лютий',
    3: 'Березень',
    4: 'Квітень',
    5: 'Травень',
    6: 'Червень',
    7: 'Липень',
    8: 'Серпень',
    9: 'Вересень',
    10: 'Жовтень',
    11: 'Листопад',
    12: 'Грудень',
}

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
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7,
}


@login_required(redirect_field_name='next')
@tutor_type_only
def change_month_timetable_tutor(request):
    current_year = datetime.today().year
    current_month = datetime.today().month

    tutor = request.user.profile.protutor

    # 0 - monday, 6 - sunday
    # first_day_week, length_month = 5, 31
    first_day_week, length_month = calendar.monthrange(current_year, current_month)

    action = request.POST.get('action')

    if request.POST and action == 'Зберегти зміни':

        # save new default work time
        selected_time_dict = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [],
                              "Saturday": [], "Sunday": []}

        for answer in request.POST:
            if "1_" in answer:
                selected_time_dict["Monday"].append(request.POST[answer])
            elif "2_" in answer:
                selected_time_dict["Tuesday"].append(request.POST[answer])
            elif "3_" in answer:
                selected_time_dict["Wednesday"].append(request.POST[answer])
            elif "4_" in answer:
                selected_time_dict["Thursday"].append(request.POST[answer])
            elif "5_" in answer:
                selected_time_dict["Friday"].append(request.POST[answer])
            elif "6_" in answer:
                selected_time_dict["Saturday"].append(request.POST[answer])
            elif "7_" in answer:
                selected_time_dict["Sunday"].append(request.POST[answer])

        try:
            def_obj = SelectedWorkingHoursByDefault.objects.get(tutor_fk=tutor)
            default_hours_dict = json.loads(def_obj.selected_time)
            if default_hours_dict != selected_time_dict:
                default_hours_dict = json.dumps(selected_time_dict)
                def_obj.selected_time = default_hours_dict
                def_obj.save()
        except SelectedWorkingHoursByDefault.DoesNotExist:
            default_hours_dict = json.dumps(selected_time_dict)
            SelectedWorkingHoursByDefault.objects.create(tutor_fk=tutor, selected_time=default_hours_dict)

        # save new weekdays
        request_week_day_dict = {}
        selected_time = json.loads(SelectedWorkingHoursByDefault.objects.get(tutor_fk=tutor).selected_time)

        try:
            def_obj = MonthTutorTimetable.objects.get(tutor_fk=tutor, month=current_month, year=current_year)
            old_month_selected_weekdays = json.loads(def_obj.selected_weekdays)
            old_month_booked_weekdays = json.loads(def_obj.booked_weekdays)
        except MonthTutorTimetable.DoesNotExist:
            old_month_selected_weekdays = {}
            old_month_booked_weekdays = {}

        new_working_day_list = []

        for answer in request.POST:
            if "week_day_" in answer:
                date_day = int(request.POST[answer])
                selected_date = date(current_year, current_month, date_day)

                if date.today() < selected_date:
                    new_working_day_list.append(str(date_day))
                    current_date_weekday = selected_date.weekday()

                    if 0 == current_date_weekday:
                        day_weekday = "Monday"
                        checkBookedTimeInDay(request, day_weekday, date_day, old_month_selected_weekdays, selected_time,
                                             old_month_booked_weekdays, request_week_day_dict)
                    elif 1 == current_date_weekday:
                        day_weekday = "Tuesday"
                        checkBookedTimeInDay(request, day_weekday, date_day, old_month_selected_weekdays, selected_time,
                                             old_month_booked_weekdays, request_week_day_dict)
                    elif 2 == current_date_weekday:
                        day_weekday = "Wednesday"
                        checkBookedTimeInDay(request, day_weekday, date_day, old_month_selected_weekdays, selected_time,
                                             old_month_booked_weekdays, request_week_day_dict)
                    elif 3 == current_date_weekday:
                        day_weekday = "Thursday"
                        checkBookedTimeInDay(request, day_weekday, date_day, old_month_selected_weekdays, selected_time,
                                             old_month_booked_weekdays, request_week_day_dict)
                    elif 4 == current_date_weekday:
                        day_weekday = "Friday"
                        checkBookedTimeInDay(request, day_weekday, date_day, old_month_selected_weekdays, selected_time,
                                             old_month_booked_weekdays, request_week_day_dict)
                    elif 5 == current_date_weekday:
                        day_weekday = "Saturday"
                        checkBookedTimeInDay(request, day_weekday, date_day, old_month_selected_weekdays, selected_time,
                                             old_month_booked_weekdays, request_week_day_dict)
                    elif 6 == current_date_weekday:
                        day_weekday = "Sunday"
                        checkBookedTimeInDay(request, day_weekday, date_day, old_month_selected_weekdays, selected_time,
                                             old_month_booked_weekdays, request_week_day_dict)

        # check new unworked days
        start_working_day_list = list(old_month_selected_weekdays)
        for date_day in start_working_day_list:
            if not (date_day in new_working_day_list):
                if date_day in old_month_booked_weekdays:
                    request_week_day_dict[str(date_day)] = old_month_selected_weekdays[str(date_day)]
                    messages.warning(request, f"Ви не можете відмінити робочий день за {date_day} число, "
                                              f"оскільки Студенти вже забронювали заняття з Вами!")

        try:
            def_obj = MonthTutorTimetable.objects.get(tutor_fk=tutor, month=current_month, year=current_year)
            selected_weekdays = json.loads(def_obj.selected_weekdays)
            if selected_weekdays != request_week_day_dict:
                selected_weekdays = json.dumps(request_week_day_dict)
                def_obj.selected_weekdays = selected_weekdays
                def_obj.save()
        except MonthTutorTimetable.DoesNotExist:
            selected_weekdays = json.dumps(request_week_day_dict)
            # we can change "course_fk" for many courses per tutor
            MonthTutorTimetable.objects.create(tutor_fk=tutor,
                                               selected_weekdays=selected_weekdays,
                                               month=current_month,
                                               year=current_year)
        messages.success(request, "Зміни були успішно збережені!")

    # start with 2 day of the month
    length_month_list = []
    for _ in range(2, length_month + 1):
        length_month_list.append(_)

    # for templates
    try:
        def_obj = SelectedWorkingHoursByDefault.objects.get(tutor_fk=tutor)
        default_hours_dict = json.loads(def_obj.selected_time)
        default_hours_id_list = defaultHoursIdList(default_hours_dict)
    except SelectedWorkingHoursByDefault.DoesNotExist:
        default_hours_id_list = []

    try:
        def_obj = MonthTutorTimetable.objects.get(tutor_fk=tutor, month=current_month, year=current_year)
        selected_weekdays = json.loads(def_obj.selected_weekdays)
    except MonthTutorTimetable.DoesNotExist:
        selected_weekdays = {}

    context = {
        'first_day_week': first_day_week,
        'length_month': length_month,
        'length_month_list': length_month_list,
        'name_month': NAMES_MONTHS[current_month],
        'current_year': current_year,
        'default_hours_id_list': default_hours_id_list,
        'selected_weekdays': selected_weekdays,
        'today_date': date.today().day,
    }
    return render(request, "timetable/change_month_timetable_tutor.html", context=context)


@login_required(redirect_field_name='next')
@student_type_only
def change_month_timetable_student(request, cid):
    progress = get_object_or_404(Progress, student_fk=request.user.profile.prostudent, id_course=cid)
    if check_date_access_to_course(progress):

        current_year = datetime.today().year
        current_month = datetime.today().month
        first_day_week, length_month = calendar.monthrange(current_year, current_month)

        # start with 2 day of the month
        length_month_list = []
        for _ in range(2, length_month + 1):
            length_month_list.append(_)

        progress = Progress.objects.get(id_course=cid, student_fk=request.user.profile.prostudent)

        if progress.tutor_fk is not None:
            tutor = progress.tutor_fk
            try:
                def_obj = MonthTutorTimetable.objects.get(tutor_fk=tutor, month=current_month, year=current_year)
                selected_weekdays = json.loads(def_obj.selected_weekdays)
                id_month_timetable_tutor = def_obj.id
            except MonthTutorTimetable.DoesNotExist:
                selected_weekdays = {}
                id_month_timetable_tutor = 0
        else:
            id_month_timetable_tutor = 0
            selected_weekdays = {}
            tutor = None

        if tutor is None:
            messages.info(request, "На жаль, Ви поки не маєте свого Тьютора, тому розклад занять не доступний. Не "
                                   "хвилюйтесь, ми вже вирішуємо це питання!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            bought_lessons = progress.include_month_private_lessons_current + progress.qty_bought_private_lessons
            context = {
                'bought_lessons': bought_lessons,
                'first_day_week': first_day_week,
                'length_month': length_month,
                'current_year': current_year,
                'name_month': NAMES_MONTHS[current_month],
                'length_month_list': length_month_list,
                'selected_weekdays': selected_weekdays,
                'tutor': tutor,
                'id_month_timetable_tutor': id_month_timetable_tutor,
            }
            return render(request, "timetable/change_month_timetable_student.html", context=context)
    else:
        messages.warning(request, "На жаль, Ви не маєте доступу до цього курсу. Ви можете придбати підписку нижче!")
        cid_course = get_object_or_404(Course, id=cid)
        context = {
            'course': cid_course,
            'topics': cid_course.topics.all(),
        }
        return render(request, 'course/false_access_data_view_course_student.html', context)


@login_required(redirect_field_name='next')
@student_type_only
def date_by_student(request, date_day, mtb_id):
    selected_lesson_days = {}
    month_tutor_timetable = MonthTutorTimetable.objects.get(id=mtb_id)
    name_month = NAMES_MONTHS[int(month_tutor_timetable.month)]

    current_year = datetime.today().year
    current_month = datetime.today().month

    selected_weekdays = json.loads(month_tutor_timetable.selected_weekdays)
    booked_weekdays = json.loads(month_tutor_timetable.booked_weekdays)

    unbooked_today_time_list = createUnbookedTimeList(date_day, selected_weekdays, booked_weekdays)

    action = request.POST.get('action')
    # ADD DATE CHECK !!! DAY LESSON > TODAY.DAY
    if request.POST and action == 'Забронювати місце' and 'time' in request.POST:
        request_time = request.POST['time']
        current_course = month_tutor_timetable.course_fk
        student = request.user.profile.prostudent
        progress = Progress.objects.get(student_fk=student,
                                        id_course=current_course.id)
        if progress.qty_bought_private_lessons > 0 or progress.include_month_private_lessons_current > 0:
            # create PrivateLesson
            lesson_date = date(current_year, current_month, date_day)
            private_lesson = PrivateLesson.objects.create(tutor_fk=progress.tutor_fk,
                                                          student_fk=student,
                                                          progress_fk=progress,
                                                          lesson_date=lesson_date,
                                                          lesson_time=request_time, )

            # add select_lesson_time in MonthStudentTimetable
            try:
                student_timetable = MonthStudentTimetable.objects.get(progress_fk=progress,
                                                                      month=current_month,
                                                                      year=current_year)
                selected_lesson_days = json.loads(student_timetable.selected_lesson_days)

                if str(date_day) in selected_lesson_days:
                    day_time_dict = selected_lesson_days[str(date_day)]
                else:
                    day_time_dict = {}
                day_time_dict[request_time] = progress.id
                selected_lesson_days[str(date_day)] = day_time_dict

                selected_lesson_days = json.dumps(selected_lesson_days)
                student_timetable.selected_lesson_days = selected_lesson_days
                student_timetable.save()
            except MonthStudentTimetable.DoesNotExist:
                selected_lesson_days[date_day] = {request_time: progress.id}
                selected_lesson_days = json.dumps(selected_lesson_days)
                MonthStudentTimetable.objects.create(progress_fk=progress,
                                                     student_fk=student,
                                                     course_fk=current_course,
                                                     selected_lesson_days=selected_lesson_days,
                                                     month=current_month,
                                                     year=current_year)

            # add lesson to tutor month timetable
            booked_time_dict = {}
            tutor_booked_weekdays = json.loads(month_tutor_timetable.booked_weekdays)
            if str(date_day) in tutor_booked_weekdays:
                booked_time_dict = tutor_booked_weekdays[str(date_day)]

            booked_time_dict[request_time] = private_lesson.id

            tutor_booked_weekdays[str(date_day)] = booked_time_dict

            tutor_booked_weekdays = json.dumps(tutor_booked_weekdays)
            month_tutor_timetable.booked_weekdays = tutor_booked_weekdays
            month_tutor_timetable.save()

            # increment qty bought lessons
            if progress.include_month_private_lessons_current > 0:
                progress.include_month_private_lessons_current -= 1
                progress.save()
            elif progress.qty_bought_private_lessons > 0:
                progress.qty_bought_private_lessons -= 1
                progress.save()

            # message, redirect
            messages.success(request, "Ви успішно забронювали урок. Не забудьте підготуватись до заняття!")
            return redirect('personal_cabinet')
        else:
            messages.warning(request, "Ви не можете забронювати урок, оскільки кількість придбаних уроків була "
                                      "вичерпана. Ви можете придбати додаткові уроки в особистому кабінеті.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if len(unbooked_today_time_list) == 0:
        messages.info(request, "На жаль, у цей день немає вільних годин. Спробуйте обрати іншу дату.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    elif date.today().day == date_day:
        messages.info(request, "На жаль, Ви не можете призначати урок з Тьютором в день його проведення. Спробуйте "
                               "обрати іншу дату.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'name_month': name_month,
        'date_day': date_day,
        'current_year': month_tutor_timetable.year,
        'unbooked_today_time_list': unbooked_today_time_list,
    }
    return render(request, 'timetable/day_by_student.html', context)


def defaultHoursIdList(default_hours_dict):
    default_hours_id_list = []
    for key in default_hours_dict:
        current_list = getListDayWeekTimes(key, default_hours_dict)
        if len(current_list) > 0:
            default_hours_id_list += current_list
    return default_hours_id_list


def getListDayWeekTimes(week_day, default_hours_dict):
    default_hours_id_list = []
    time_list = default_hours_dict[week_day]
    if len(time_list) > 0:
        for time in time_list:
            id_time = str(ID_DAYS[week_day]) + "_" + str(ID_DICT[time])
            default_hours_id_list.append(id_time)
    return default_hours_id_list


def createUnbookedTimeList(date_day, selected_weekdays, booked_weekdays):
    unbooked_today_time_list = []
    selected_weekday_times_list = selected_weekdays[str(date_day)]

    if str(date_day) in booked_weekdays:
        booked_weekday_times_dict = booked_weekdays[str(date_day)]
        for time in selected_weekday_times_list:
            if not (time in booked_weekday_times_dict):
                unbooked_today_time_list.append(time)
    else:
        for time in selected_weekday_times_list:
            unbooked_today_time_list.append(time)
    return unbooked_today_time_list


def sortTimeList(t):
    start_time, end_time = t.split("-")
    start_hour, start_minute = start_time.split(":")
    end_hour, end_minute = end_time.split(":")
    statement = (int(end_hour) - int(start_hour)) * 60 - (int(end_minute) - int(start_hour))
    return statement


def checkBookedTimeInDay(request, day_weekday, date_day, old_month_selected_weekdays, selected_time,
                         old_month_booked_weekdays, request_week_day_dict):
    if str(date_day) in old_month_selected_weekdays:
        start_working_time_list = old_month_selected_weekdays[str(date_day)]
        new_working_time_list = selected_time[day_weekday]
        old_day_booked_weekdays_dict = old_month_booked_weekdays[str(date_day)]

        for new_time in new_working_time_list:
            if new_time in old_day_booked_weekdays_dict:
                old_day_booked_weekdays_dict.pop(new_time)
        if len(old_day_booked_weekdays_dict) > 0:
            try_d = selected_time[day_weekday] + [time for time in old_day_booked_weekdays_dict]
            x = list(set(try_d))
            request_week_day_dict[str(date_day)] = sorted(x, key=sortTimeList)
            messages.warning(request, f"Деякий час роботи за {date_day} число не було змінено, "
                                      f"оскільки Студенти вже забронювали заняття з Вами! Новий "
                                      f"час було додано!")
        else:
            request_week_day_dict[str(date_day)] = selected_time[day_weekday]
    else:
        request_week_day_dict[str(date_day)] = selected_time[day_weekday]
