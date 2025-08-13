from django.db import models

class Notice(models.Model):
    admin_id = models.IntegerField(default=14)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  

  
