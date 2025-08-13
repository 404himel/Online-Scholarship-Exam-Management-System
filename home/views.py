from django.shortcuts import render

# Create your views here.

def home1(request):
    return render(request,'index.html')
