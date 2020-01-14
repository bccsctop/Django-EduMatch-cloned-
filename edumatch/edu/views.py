from django.shortcuts import render,redirect
from django.http import HttpResponse
from edu.models import Tutor,Selected_Subject
# Create your views here.
def home_page(request):
    if request.method == 'POST':
        Selected_Subject.objects.create(subject=request.POST['subject_text'])
        return redirect('/')
    
    tutors = Tutor.objects.all()
    return render(request,'home.html',{
        'tutors':tutors
    })