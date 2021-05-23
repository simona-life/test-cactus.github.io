from django.contrib import admin
from access.models import (Payment,
                           Progress)


admin.site.register(Payment)
admin.site.register(Progress)
