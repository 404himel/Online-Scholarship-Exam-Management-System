from django.contrib import admin
from .models import result

@admin.register(result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'name', 'school', 'umark')
    search_fields = ('name', 'school', 'uid')

