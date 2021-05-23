from django.contrib import admin
from send_emails.models import (FromEmailSendgrit,
                                AdminEmailForEmails)


admin.site.register(FromEmailSendgrit)
admin.site.register(AdminEmailForEmails)
