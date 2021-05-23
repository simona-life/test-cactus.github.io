from django.db import models


class FromEmailSendgrit(models.Model):
    email = models.EmailField(blank=False)


class AdminEmailForEmails(models.Model):
    email = models.EmailField(blank=False)
