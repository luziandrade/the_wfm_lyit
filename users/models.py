from django.db import models
from django.contrib.auth.models import AbstractUser, Group, User
from django.conf import settings


class Resource(models.Model):
    ROLE = [
        ('Analyst', "Analyst"),
        ('Team Manager', "Team Manager"),
        ('Quality Auditor', "Quality Auditor"),
        ('Senior Analyst', "Senior Analyst"),
        ('', "")
    ]
    status = models.IntegerField(default=1)
    username = models.CharField(max_length=254, default='')
    email_sent = models.IntegerField(default=0)
    name = models.CharField(max_length=254, default='')
    surname = models.CharField(max_length=254, default='')
    role = models.CharField(max_length=30, choices=ROLE, default='')
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.username


