from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders

# Create your views here.
    
def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')
            
            Genders.objects.create(gender=gender).save()
            messages.success(request, 'Gender added na, boi!')
            return render(request, 'gender/AddGender.html')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f'Error tanga: {e}')