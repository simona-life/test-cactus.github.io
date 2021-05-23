from django.contrib import admin
from course.models import (HomeWorkPhotos,
                           AnswerQuestion,
                           Question,
                           Course,
                           Topic,
                           Lesson,
                           Text,
                           File,
                           Video,
                           Image,
                           Content)


class CourseAdmin(admin.ModelAdmin):
    list_display_links = ('title',)
    list_display = list_display_links + ('id', 'grade', 'type_grade')
    list_filter = ('grade',)
    search_fields = ('title',)
    readonly_fields = ('all_topics', 'all_lessons', 'id', 'created', 'updated')

    def all_topics(self, obj):
        c_topics = ''
        for topic in obj.topics.all():
            c_topics += str(topic.id) + topic.title + '\n'
        return c_topics

    def all_lessons(self, obj):
        c_lessons = ''
        for topic in obj.topics.all():
            lessons = topic.lessons.all()
            for lesson in lessons:
                c_lessons += str(lesson.id) + lesson.title + '\n'
        return c_lessons


class TopicAdmin(admin.ModelAdmin):
    list_display_links = ('title',)
    list_display = list_display_links + ('id', 'grade', 'type_grade')
    list_filter = ('grade',)
    search_fields = ('title',)
    readonly_fields = ('all_lessons', 'id', 'created', 'updated')

    def all_lessons(self, obj):
        c_lessons = ''
        for lesson in obj.lessons.all():
            c_lessons += str(lesson.id) + lesson.title + '\n'
        return c_lessons


class LessonAdmin(admin.ModelAdmin):
    list_display_links = ('title',)
    list_display = list_display_links + ('id', 'grade', 'type_grade')
    list_filter = ('grade',)
    search_fields = ('title',)
    readonly_fields = ('id', 'created', 'updated', 'contents')

    def contents(self, obj):
        c_contents = ''
        for content in obj.contents.all():
            c_contents += str(content.id) + content.title + '\n'
        return c_contents


admin.site.register(Text)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(File)
admin.site.register(Content)
admin.site.register(Question)
admin.site.register(AnswerQuestion)
admin.site.register(HomeWorkPhotos)

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Topic, TopicAdmin)
