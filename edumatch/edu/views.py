from django.shortcuts import render,redirect
from django.http import HttpResponse
from edu.models import Tutor,Selected_Subject
# Create your views here.
def home_page(request):
    if request.method == 'POST':
        Selected_Subject.objects.create(subject=request.POST['subject_text'])
        return redirect('/')
        
    if Selected_Subject.objects.last() is None:
        tutors = Tutor.objects.all()
        return render(request,'home.html',{
        'tutors':tutors
        })

    saved_tutors = Selected_Subject.objects.last()
    tutors = Tutor.objects.filter(expert=saved_tutors.subject)
    return render(request,'home.html',{
        'tutors':tutors
    })

def register(request):
    return redirect('/spark/register')
    return render(request, 'register.html')