from django.db import models

class result(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.BigIntegerField(unique=True)  # Removed max_length
    name = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    umark = models.CharField(max_length=15)

    class Meta:
        db_table = "result"