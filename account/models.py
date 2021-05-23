from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator

from course.models import Course

User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(null=True, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    TYPE_GENDER_CHOICES = (
        ('male', 'Чоловіча'),
        ('female', 'Жіноча'),
        ('other', 'Інше'),
    )
    TYPE_USER_CHOICES = (
        ('head-teacher', 'Хед-тічер'),
        ('tutor', 'Тьютор'),
        ('student', 'Студент'),
        ('parent', 'Батьки'),
        ('guest', 'Гість')
    )
    type_user = models.CharField(max_length=15, choices=TYPE_USER_CHOICES)
    gender = models.CharField(max_length=15, choices=TYPE_GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class ProHeadTeacher(models.Model):
    profile = models.OneToOneField('account.Profile',
                                   on_delete=models.CASCADE)
    courses = models.ManyToManyField('course.Course',
                                     related_name='headteachers')


class ProTutor(models.Model):
    profile = models.OneToOneField('account.Profile',
                                   on_delete=models.CASCADE)
    chose_qty_students = models.PositiveIntegerField(default=1,
                                                     validators=[
                                                         MinValueValidator(1),
                                                         MaxValueValidator(10),
                                                     ])
    head_teacher_fk = models.ForeignKey('account.ProHeadTeacher',
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        related_name='tutors')
    courses = models.ManyToManyField('course.Course',
                                     related_name='tutors')


class ProStudent(models.Model):
    profile = models.OneToOneField('account.Profile',
                                   on_delete=models.CASCADE)

    parent_fk = models.ForeignKey('account.ProParent',
                                  blank=True,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  related_name='students')
    GRADE_CHOICES = (
        ('ZNO', 'ЗНО'),
        ('11', '11'),
        ('10', '10'),
        ('9', '9'),
        ('8', '8'),
        ('7', '7'),
        ('6', '6'),
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
    )
    TYPE_GRADE_CHOICES = (
        ('ZNO', 'ЗНО'),
        ('in-depth', 'Поглиблене вивчення'),
        ('normal', 'Рівень стандарту'),
    )
    grade = models.CharField(max_length=15, choices=GRADE_CHOICES, default='ZNO')
    type_grade = models.CharField(max_length=15, choices=TYPE_GRADE_CHOICES, default='normal')


class ProParent(models.Model):
    profile = models.OneToOneField('account.Profile',
                                   on_delete=models.CASCADE)
