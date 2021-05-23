from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator


class DefaultLines(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField()
    finished = models.BooleanField(default=False)

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
        ('standart', 'Рівень стандарту'),
    )
    grade = models.CharField(max_length=15, choices=GRADE_CHOICES, default='ZNO')
    type_grade = models.CharField(max_length=15, choices=TYPE_GRADE_CHOICES, default='ZNO')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Course(DefaultLines):
    price = models.PositiveIntegerField(default=0)
    include_month_private_lessons_default = models.PositiveIntegerField(default=0)
    price_private_lesson = models.PositiveIntegerField(default=0)


class Topic(DefaultLines):
    course_fk = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='topics')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class Lesson(DefaultLines):
    LESSON_TYPES = (
        ('class_work', 'Класна робота'),
        ('home_work', 'Домашня робота'),
        ('explanation_home_work', 'Пояснення домашньої роботи'),
        ('control_work', 'Контрольна робота'),
    )
    type_lesson = models.CharField(max_length=30, choices=LESSON_TYPES, default='class_work')
    topic_fk = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name='lessons')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class Content(models.Model):
    lesson_fk = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='contents')
    order = models.PositiveIntegerField(default=0)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': ('Text',
                                                                     'Video',
                                                                     'Image',
                                                                     'File')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    text = models.TextField()


class Image(ItemBase):
    file = models.ImageField(upload_to='images')


class Video(ItemBase):
    file = models.FileField(upload_to="video/%y")


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Question(models.Model):
    lesson_fk = models.ForeignKey('course.Lesson',
                                  on_delete=models.CASCADE,
                                  related_name='questions')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    points = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    ANSWER_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    correct_answer = models.CharField(max_length=2, choices=ANSWER_CHOICES, default='A')

    class Meta:
        ordering = ['order']


class AnswerQuestion(models.Model):
    question_fk = models.ForeignKey('course.Question',
                                    on_delete=models.CASCADE,
                                    related_name='answers_questions')
    student_fk = models.ForeignKey('account.ProStudent',
                                   on_delete=models.CASCADE,
                                   related_name='answers_questions')
    chose_answer = models.CharField(max_length=2, default='A')
    created = models.DateTimeField(auto_now_add=True)
    points = models.PositiveIntegerField(default=0)


class HomeWorkPhotos(models.Model):
    image = models.ImageField(upload_to='images/home_work', null=True, blank=True)
    student_fk = models.ForeignKey('account.ProStudent',
                                   on_delete=models.CASCADE,
                                   related_name='homework_photos')
    lesson_fk = models.ForeignKey('course.Lesson',
                                  on_delete=models.CASCADE,
                                  related_name='homework_photos')
    created = models.DateTimeField(auto_now_add=True)
