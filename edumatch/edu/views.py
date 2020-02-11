from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from edu.models import Tutor,Selected_Subject
from edu.forms import SignUpForm
# Create your views here.
def home_page(request):
    if request.POST.get('subject_text', '') != '' and request.POST.get('gender_text', '') != '' and request.POST.get('city_text', '') != '':

        tutors = Tutor.objects.filter(expert=request.POST['subject_text'],gender=request.POST['gender_text'],city=request.POST['city_text'])
        return render(request,'home.html',{
        'tutors':tutors
        })
    
    if request.POST.get('subject_text', '') != '' and request.POST.get('gender_text', '') != '':

        tutors = Tutor.objects.filter(expert=request.POST['subject_text'],gender=request.POST['gender_text'])
        return render(request,'home.html',{
        'tutors':tutors
        })

    if request.POST.get('subject_text', '') != '' and request.POST.get('city_text', '') != '':

        tutors = Tutor.objects.filter(expert=request.POST['subject_text'],city=request.POST['city_text'])
        return render(request,'home.html',{
        'tutors':tutors
        })

    if request.POST.get('gender_text', '') != '' and request.POST.get('city_text', '') != '':

        tutors = Tutor.objects.filter(gender=request.POST['gender_text'],city=request.POST['city_text'])
        return render(request,'home.html',{
        'tutors':tutors
        })

    if request.POST.get('subject_text', '') != '':

        tutors = Tutor.objects.filter(expert=request.POST['subject_text'])
        return render(request,'home.html',{
        'tutors':tutors
        })
    
    if request.POST.get('gender_text', '') != '':

        tutors = Tutor.objects.filter(gender=request.POST['gender_text'])
        return render(request,'home.html',{
        'tutors':tutors
        })

    if request.POST.get('city_text', '') != '':

        tutors = Tutor.objects.filter(city=request.POST['city_text'])
        return render(request,'home.html',{
        'tutors':tutors
        })
        
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