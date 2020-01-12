from django.shortcuts import render
from django.http import HttpResponse
from edu.models import Tutor
# Create your views here.
def home_page(request):
    tutors = Tutor.objects.all()
    return render(request,'home.html',{
        'tutors':tutors
    })