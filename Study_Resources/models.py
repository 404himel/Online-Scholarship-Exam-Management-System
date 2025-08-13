# models.py
from django.db import models

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('book', 'Book'),
        ('video', 'Video'),
        ('doc', 'Documentation'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
