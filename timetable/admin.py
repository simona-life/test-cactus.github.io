from django.contrib import admin

from timetable.models import (MonthTutorTimetable,
                              MonthStudentTimetable,
                              SelectedWorkingHoursByDefault)


admin.site.register(MonthStudentTimetable)
admin.site.register(MonthTutorTimetable)
admin.site.register(SelectedWorkingHoursByDefault)
