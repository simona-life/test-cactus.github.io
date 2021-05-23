from django import forms
from django.contrib.auth.models import User
from account.formfield import PhoneNumberField
from django.core.exceptions import ValidationError

from account.models import Profile


def validate_email_exist(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError("Юзер з таким e-mail вже існує")


def validate_phone_number_exist(phone_number):
    if Profile.objects.filter(phone_number=phone_number).exists():
        raise ValidationError("Юзер з таким номером телефону вже існує")


class ParentFormFirstBuy(forms.Form):
    first_name_student = forms.CharField(label="Ім'я студента", max_length=20)
    last_name_student = forms.CharField(label='Призвіще студента', max_length=20)
    email_student = forms.CharField(label='E-mail студента', validators=[validate_email_exist])
    phone_number_student = PhoneNumberField(label="Номер телефону студента",  validators=[validate_phone_number_exist])


class StudentFormFirstBuy(forms.Form):
    pass
