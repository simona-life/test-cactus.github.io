from django.urls import path, include
from account import views

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from account.views import (tutor_info,
                           personal_cabinet,
                           parents_students_view,
                           tutor_personal_cabinet,
                           parent_personal_cabinet,
                           student_personal_cabinet,
                           head_teacher_personal_cabinet,
                           sid_student_info_for_parent)


urlpatterns = [

    # login, logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    # personal cabinets
    path('', personal_cabinet, name='personal_cabinet'),

    path('student_personal_cabinet/', student_personal_cabinet, name='student_personal_cabinet'),
    path('parent_personal_cabinet/', parent_personal_cabinet, name='parent_personal_cabinet'),

    path('parents_students_view/', parents_students_view, name='parents_students_view'),

    path('tutor_personal_cabinet/', tutor_personal_cabinet, name='tutor_personal_cabinet'),
    path('head_teacher_personal_cabinet/', head_teacher_personal_cabinet, name='head_teacher_personal_cabinet'),
    path('student/<int:sid>/student_info_for_parent/', sid_student_info_for_parent, name='sid_student_info_for_parent'),

    path('<int:tid>/tutor_info/', tutor_info, name='tutor_info'),

    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),

    # change password
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # reset password
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             email_template_name='registration/password_reset_email1.html', from_email='vavolan@gmail.com'
         ),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
