from django.shortcuts import render
from .models import result


def result_view(request):
    
    sort_order = request.GET.get('sort', 'desc')  
    schools = None

    if request.method=="POST":
         schools = request.POST.get('school')
    
    
    userdata = result.objects.all()

    
    if schools:
        userdata = userdata.filter(school__iexact=schools)

    if sort_order == 'asc':
        userdata = userdata.order_by('umark')  
    else:
        userdata = userdata.order_by('-umark')  

    

    return render(request, 'result.html', {'userdata': userdata})
