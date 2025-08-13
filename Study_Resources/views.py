# views.py
from django.shortcuts import render
from Study_Resources.models import Resource 

def resource_page(request):
    books = Resource.objects.filter(category='book')
    videos = Resource.objects.filter(category='video')
    docs = Resource.objects.filter(category='doc')
    others = Resource.objects.filter(category='other')

    return render(request, 'resource_page.html', {
        'books': books,
        'videos': videos,
        'docs': docs,
        'others': others,
    })
