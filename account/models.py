from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    SCHOOL_CHOICES = [
        ('school_1', 'School 1'),
        ('school_2', 'School 2'),
        ('school_3', 'School 3'),
        ('school_4', 'School 4'),
        ('school_5', 'School 5'),
    ]
    
    school = models.CharField(max_length=255, choices=SCHOOL_CHOICES, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    roll_no = models.IntegerField(blank=True, null=True)


class Delete(models.Model):
    username =  models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)


