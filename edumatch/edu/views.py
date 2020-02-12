from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from edu.models import Tutor,Selected_Subject
from edu.forms import SignUpForm
# Create your views here.
def home_page(request):

    tutors = Tutor.objects.all()

    subject = request.POST.get('subject_text','')
    gender = request.POST.get('gender_text','')
    city = request.POST.get('city_text','')

    tutors = tutors.filter(expert=subject) if subject != '' else tutors
    tutors = tutors.filter(gender=gender) if gender != '' else tutors
    tutors = tutors.filter(city=city) if city != '' else tutors
    tutors = tutors.exclude(user=request.user) if request.user.is_authenticated else tutors
    if request.user.is_authenticated:
        tutors = tutors.exclude(user=request.user)

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
           
            tutor = Tutor.objects.create(user=user, name=form.cleaned_data['first_name'], gender=form.cleaned_data['gender'], city=form.cleaned_data['city'], expert=form.cleaned_data['subject'])

            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def tutor_list(request,tutor_id):
    tutors = Tutor.objects.all().exclude(id=tutor_id)
    return render(request,'list.html',{
        'tutors':tutors
    })

def profile(request):
    tutors = Tutor.objects.get(user=request.user)
    tutors_city = tutors.city
    tutors_gender = tutors.gender
    tutors_expert = tutors.expert
    #test = Tutor.objects.get(user = request.user)
    return render(request,'profile.html',{
        'user':request.user,'tutors':tutors,'city':tutors_city,'gender':tutors.gender,'expert':tutors.expert
    })
