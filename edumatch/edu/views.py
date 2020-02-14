from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from edu.models import Tutor,Matched_Request
from edu.forms import SignUpForm , EditProfileForm
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

def view_profile(request):
    tutors = Tutor.objects.get(user=request.user)
    tutors_city = tutors.city
    tutors_gender = tutors.gender
    tutors_expert = tutors.expert
    #test = Tutor.objects.get(user = request.user)
    return render(request,'profile.html',{
        'user':request.user,'tutors':tutors,'city':tutors_city,'gender':tutors.gender,'expert':tutors.expert
    })
def edit_profile(request):
    tutors = Tutor.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST,instance = request.user)
        if form.is_valid() :
            form.save()
            view_profile(request)
            return redirect('profile')
    else:    
        form = EditProfileForm(instance = request.user)
        return render(request,'edit_profile.html',{'form':form})
        

def send_match_request(request, tutor_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=tutor_id)
        matchUser = Tutor.objects.filter(name='Ronnie')
        for i in matchUser:
            i.isMatched = 'True'
            i.save()
        frequest, created = Matched_Request.objects.get_or_create(
        from_user=request.user, to_user=user)
        return HttpResponseRedirect('/')


def cancel_match_request(request, tutor_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=tutor_id)
        matchUser = Tutor.objects.filter(name='Ronnie')
        for i in matchUser:
            i.isMatched = 'False'
            i.save()
        frequest = Matched_Request.objects.filter(
        from_user=request.user, to_user=user).first()
        frequest.delete()
        return HttpResponseRedirect('/')

def accept_match_request(request, tutor_id):
	from_user = get_object_or_404(User, id=tutor_id)
	frequest = Matched_Request.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.tutor.groupMatch.add(user2.tutor)
	user2.tutor.groupMatch.add(user1.tutor)
	frequest.delete()
	return HttpResponseRedirect('/match-result/1')

def delete_match_request(request, tutor_id):
	from_user = get_object_or_404(User, id=tutor_id)
	frequest = Matched_Request.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return HttpResponseRedirect('/match-result/1')

def match_result(request,tutor_id):
	p = Tutor.objects.filter(id=tutor_id).first()
	u = p.user
	sent_match_requests = Matched_Request.objects.filter(from_user=p.user)
	rec_match_requests = Matched_Request.objects.filter(to_user=p.user)

	contact = p.groupMatch.all()

	context = {
		'u': u,
		'contact_list': contact,
		'sent_match_requests': sent_match_requests,
		'rec_match_requests': rec_match_requests
	}

	return render(request, "manage_match.html", context)
