from django.shortcuts import render
from .models import Notice

def notice(request):
    notices = Notice.objects.all()  
    return render(request, 'notice.html', {'notices': notices})
