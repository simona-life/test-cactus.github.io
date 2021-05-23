from django import forms
from django.contrib.auth.models import User
from account.formfield import PhoneNumberField
from access.forms import validate_phone_number_exist
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from account.models import Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Юзернейм", help_text="Юзернейм може мати букви, цифри та знаки @/./+/-/_ ")
    email = forms.EmailField(label="E-mail")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Підтвердіть пароль", help_text='Введіть пароль ще раз',
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Паролі не збігаються!')
        return cd['password2']


class ProfileRegisterForm(forms.ModelForm):
    phone_number = PhoneNumberField(label="Номер телефону",  validators=[validate_phone_number_exist])

    class Meta:
        model = Profile
        fields = ('phone_number',)


class UserEditForm(forms.ModelForm):
    username = forms.CharField(label="Юзернейм юзера", help_text="Юзернейм може мати букви, цифри та знаки @/./+/-/_ ")
    email = forms.EmailField(label="E-mail")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    TYPE_GENDER_CHOICES = (
        ('male', 'Чоловіча'),
        ('female', 'Жіноча'),
        ('other', 'Інше'),
    )
    gender = forms.ChoiceField(label='Стать', required=False, choices=TYPE_GENDER_CHOICES)
    phone_number = PhoneNumberField(label="Номер телефону")
    photo = forms.ImageField(label='Аватар', required=False)
    date_of_birth = forms.DateField(label='Дата народження', help_text="Формат 27.12.1990")

    class Meta:
        model = Profile
        fields = ('phone_number', 'photo', 'date_of_birth', 'gender')
