from django.shortcuts import render,redirect
from django.http import HttpResponse
from edu.models import Tutor,Selected_Subject
# Create your views here.
def home_page(request):
    tutors = Tutor.objects.all()
    return render(request,'home.html',{
        'tutors':tutors
    })

def register(request):
    if request.method == 'POST':
        return redirect('/register')
    #return redirect('/register')
    return render(request, 'register.html')