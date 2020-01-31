from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from edu.models import Tutor,Selected_Subject
from edu.forms import SignUpForm
# Create your views here.
def home_page(request):
    tutors = Tutor.objects.all()
    return render(request,'home.html',{
        'tutors':tutors
    })

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def tutor_list(request,tutor_id):
    tutors = Tutor.objects.all().exclude(id=tutor_id)
    return render(request,'list.html',{
        'tutors':tutors
    })