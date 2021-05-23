from datetime import datetime
from django.template import Context
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from course.models import Course
from account.models import (Profile,
                            ProTutor,
                            ProParent,
                            ProStudent,
                            ProHeadTeacher)
from send_emails.models import (FromEmailSendgrit,
                                AdminEmailForEmails)


def get_from_emails_list():
    all_from_emails_obj = FromEmailSendgrit.objects.all()
    FROM_EMAILS = []
    for email in all_from_emails_obj:
        FROM_EMAILS.append(email)
    return FROM_EMAILS


def get_admins_emails_list():
    admin_emails_obj = AdminEmailForEmails.objects.all()
    ADMIN_EMAILS = []
    for email in admin_emails_obj:
        ADMIN_EMAILS.append(email)
    return ADMIN_EMAILS


def new_tutor_by_headteacher_for_admin_mail(headteacher_id, new_tutor_id, course_id, to_email):

    # headteacher info
    headteacher = ProHeadTeacher.objects.get(id=headteacher_id)
    headteacher_profile = headteacher.profile
    first_name_headteacher = headteacher_profile.user.first_name
    last_name_headteacher = headteacher_profile.user.first_name
    phone_number_headteacher = headteacher_profile.phone_number
    username_headteacher = headteacher_profile.user.username
    headteacher_email = headteacher_profile.user.email

    # tutor info
    new_tutor = ProTutor.objects.get(id=new_tutor_id)
    new_tutor_profile = new_tutor.profile
    first_name_new_tutor = new_tutor_profile.user.first_name
    last_name_new_tutor = new_tutor_profile.user.first_name
    phone_number_new_tutor = new_tutor_profile.phone_number
    username_new_tutor = new_tutor_profile.user.username
    email_new_tutor = new_tutor_profile.user.email

    # course info
    course = Course.objects.get(id=course_id)
    course_title = course.title

    # to_email to list
    to_email = [to_email]

    for from_email in get_from_emails_list():
        try:
            mail = EmailMultiAlternatives(
                subject=f"{first_name_headteacher} {last_name_headteacher} додав/додала нового Тьютора",
                body=f"Новий Тьютор на курсі {course_title}!",
                from_email=f"Дмитро CactusEra <{from_email}>",
                to=to_email,  # []
            )

            context = {
                'first_name_headteacher': first_name_headteacher,
                'last_name_headteacher': last_name_headteacher,
                'phone_number_headteacher': phone_number_headteacher,
                'username_headteacher': username_headteacher,
                'headteacher_email': headteacher_email,

                'first_name_new_tutor': first_name_new_tutor,
                'last_name_new_tutor': last_name_new_tutor,
                'phone_number_new_tutor': phone_number_new_tutor,
                'username_new_tutor': username_new_tutor,
                'email_new_tutor': email_new_tutor,

                'course_title': course_title,
            }

            data_for_template = Context(context)
            email_html = get_template("new_tutor_by_headteacher_for_admin_mail.html")
            html_content = email_html.render(data_for_template)
            mail.attach_alternative(html_content, "text/html")

            mail.categories = [
                'work',
                'urgent',
            ]
            mail.send()
            break
        except:
            pass


def email_for_new_tutor(headteacher_id, new_tutor_id, course_id, to_email):
    # headteacher info
    headteacher = ProHeadTeacher.objects.get(id=headteacher_id)
    headteacher_profile = headteacher.profile
    first_name_headteacher = headteacher_profile.user.first_name
    last_name_headteacher = headteacher_profile.user.first_name
    phone_number_headteacher = headteacher_profile.phone_number
    username_headteacher = headteacher_profile.user.username
    headteacher_email = headteacher_profile.user.email

    # tutor info
    new_tutor = ProTutor.objects.get(id=new_tutor_id)
    new_tutor_profile = new_tutor.profile
    first_name_new_tutor = new_tutor_profile.user.first_name
    last_name_new_tutor = new_tutor_profile.user.first_name
    phone_number_new_tutor = new_tutor_profile.phone_number
    username_new_tutor = new_tutor_profile.user.username
    email_new_tutor = new_tutor_profile.user.email

    # course info
    course = Course.objects.get(id=course_id)
    course_title = course.title

    # to_email to list
    to_email = [to_email]

    for from_email in get_from_emails_list():
        try:
            mail = EmailMultiAlternatives(
                subject=f"{first_name_headteacher} {last_name_headteacher} призначив Вас Тьютором!",
                body=f'Вітаємо! Тепер Ви - Тьютор курсу "{course_title}!"',
                from_email=f"Дмитро CactusEra <{from_email}>",
                to=to_email,  # []
            )

            context = {
                'first_name_headteacher': first_name_headteacher,
                'last_name_headteacher': last_name_headteacher,
                'phone_number_headteacher': phone_number_headteacher,
                'username_headteacher': username_headteacher,
                'headteacher_email': headteacher_email,

                'first_name_new_tutor': first_name_new_tutor,
                'last_name_new_tutor': last_name_new_tutor,
                'phone_number_new_tutor': phone_number_new_tutor,
                'username_new_tutor': username_new_tutor,
                'email_new_tutor': email_new_tutor,

                'course_title': course_title,
            }

            data_for_template = Context(context)
            email_html = get_template("email_for_new_tutor.html")
            html_content = email_html.render(data_for_template)
            mail.attach_alternative(html_content, "text/html")

            mail.categories = [
                'work',
            ]
            mail.send()
            break
        except:
            pass


def dismiss_email_for_tutor(tutor_id, to_email):

    # tutor info
    tutor = ProTutor.objects.get(id=tutor_id)
    tutor_profile = tutor.profile
    first_name_tutor = tutor_profile.user.first_name
    last_name_tutor = tutor_profile.user.first_name

    # to_email to list
    to_email = [to_email]

    for from_email in get_from_emails_list():
        try:
            mail = EmailMultiAlternatives(
                subject=f"Лист про Ваше звільнення",
                body=f'На жаль, Вас було звільненно. Читайте більше інформації нижче!',
                from_email=f"Дмитро CactusEra <{from_email}>",
                to=to_email,  # []
            )

            context = {

                'first_name_new_tutor': first_name_tutor,
                'last_name_new_tutor': last_name_tutor,

            }

            data_for_template = Context(context)
            email_html = get_template("dismiss_email_for_tutor.html")
            html_content = email_html.render(data_for_template)
            mail.attach_alternative(html_content, "text/html")

            mail.categories = [
                'work',
            ]
            mail.send()
            break
        except:
            pass


def dismiss_email_about_tutor_for_headteacher(tutor_id, to_email):
    # tutor info
    tutor = ProTutor.objects.get(id=tutor_id)
    tutor_profile = tutor.profile
    first_name_tutor = tutor_profile.user.first_name
    last_name_tutor = tutor_profile.user.first_name

    # to_email to list
    to_email = [to_email]

    # courses info
    courses = tutor.courses.all()
    courses_titles = 'Курси: '
    for course in courses:
        courses_titles += f'"{course.title}"; '

    for from_email in get_from_emails_list():
        try:
            mail = EmailMultiAlternatives(
                subject=f"Лист про ",
                body=f'На жаль, Вас було звільненно. Читайте більше інформації нижче!',
                from_email=f"Дмитро CactusEra <{from_email}>",
                to=to_email,  # []
            )

            context = {

                'first_name_new_tutor': first_name_tutor,
                'last_name_new_tutor': last_name_tutor,
                'courses_titles': courses_titles,
            }

            data_for_template = Context(context)
            email_html = get_template("dismiss_email_about_tutor_for_headteacher.html")
            html_content = email_html.render(data_for_template)
            mail.attach_alternative(html_content, "text/html")

            mail.categories = [
                'work',
            ]
            mail.send()
            break
        except:
            pass


def dismiss_email_about_tutor_for_admin(tutor_id, to_email):
    # tutor info
    tutor = ProTutor.objects.get(id=tutor_id)
    tutor_profile = tutor.profile
    first_name_tutor = tutor_profile.user.first_name
    last_name_tutor = tutor_profile.user.first_name

    # to_email to list
    to_email = [to_email]

    # courses info
    courses = tutor.courses.all()
    courses_titles = 'Курси: '
    for course in courses:
        courses_titles += f'"{course.title}"; '

    for from_email in get_from_emails_list():
        try:
            mail = EmailMultiAlternatives(
                subject=f"Лист про ",
                body=f'На жаль, Вас було звільненно. Читайте більше інформації нижче!',
                from_email=f"Дмитро CactusEra <{from_email}>",
                to=to_email,  # []
            )

            context = {

                'first_name_new_tutor': first_name_tutor,
                'last_name_new_tutor': last_name_tutor,
                'courses_titles': courses_titles,
            }

            data_for_template = Context(context)
            email_html = get_template("dismiss_email_about_tutor_for_admin.html")
            html_content = email_html.render(data_for_template)
            mail.attach_alternative(html_content, "text/html")

            mail.categories = [
                'work',
            ]
            mail.send()
            break
        except:
            pass