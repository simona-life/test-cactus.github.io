from django.contrib import admin
from account.models import (Profile,
                            ProTutor,
                            ProHeadTeacher,
                            ProParent,
                            ProStudent)


admin.site.register(Profile)
admin.site.register(ProTutor)
admin.site.register(ProHeadTeacher)
admin.site.register(ProStudent)
admin.site.register(ProParent)

