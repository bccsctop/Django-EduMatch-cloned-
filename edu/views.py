from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from edu.models import Tutor, Matched_Request, Review
from edu.forms import SignUpForm, EditProfileForm, EditProfileForm2, ReviewForm, CITY_CHOICES
import time
import datetime
# Create your views here.


def home_page(request):
    if not request.user.is_authenticated:  #Check that user is logged in.
        return redirect('login')           #If user is not logged in to the server page will redirect to login page

    tutors = Tutor.objects.all()                     #Get Tutor object and store in tutors variable
    subject = request.POST.get('subject_text', '')   #Get subject_text in the search box and store in subject variable
    gender = request.POST.get('gender_text', '')     #Get gender_text at dropdown  and store in gender variable
    city = request.POST.get('city_text', '')         #Get city_text at dropdown and store in city variable

    cities = [i[0] for i in CITY_CHOICES]                                   #Store CITY_CHOICES that are declare in form.py to cities variable
    tutors = tutors.filter(expert=subject) if subject != '' else tutors     #If subject is existed tutors will filter user that in condition.
    tutors = tutors.filter(gender=gender) if gender != '' else tutors       #If gender is existed tutors will filter user that in condition.
    tutors = tutors.filter(city=city) if city != '' else tutors             #If city is existed tutors will filter user that in condition.
    tutors = tutors.exclude(user=request.user)                              #Take off the current user that is logged in out of tutors
    current_user = Tutor.objects.get(user=request.user)                     #Get current user and store to current_user

    for match_user in current_user.groupMatch.all():                                    #Take off the user that already match with current user
        tutors = tutors.exclude(pk=match_user.id)

    rec_match_requests = Matched_Request.objects.filter(to_user=current_user.user)      #Filter the Match_Request that current user recieve request
    get_match_requests = Matched_Request.objects.filter(from_user=current_user.user)    #Filter the Match_Request that current user sent request to other user
    
    requestedTutor = []
    unrequestedTutor = []
    for i in tutors:                                #Check the user that curent user already sent the request
        numCount = 0
        for j in get_match_requests:
            if i.name == j.to_user.first_name:
                requestedTutor.append(i)            #current user alreadr send the request 
                numCount+=1
        if numCount == 0:
            unrequestedTutor.append(i)              #current user never send the request

    if len(rec_match_requests) > 0 :                #If current user have recieve request
        return render(request, 'home.html', {
                'requestedTutor': requestedTutor,
                'unrequestedTutor': unrequestedTutor,
                'amountRecieve': len(rec_match_requests),
                'current_user': current_user,
                'cites':cities
            })

    return render(request, 'home.html', {           #If current user not have recieve request
        'requestedTutor': requestedTutor,
        'unrequestedTutor': unrequestedTutor,
        'current_user': current_user,
        'cities':cities
    })


def register(request):
    """ In register method, it will create user with data from SignUpForm in forms.py.
    Before we save user to database we have to check the data is validated.
    If form is validated we will create user as a object with
    user, name, gender, city, subject.
    """
    if request.method == 'POST':                
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            tutor = Tutor.objects.create(user=user, name=form.cleaned_data['first_name'], gender=form.cleaned_data[
                                         'gender'], city=form.cleaned_data['city'], expert=form.cleaned_data['subject'])

            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def view_profile(request):
    """ In view_profile, it will get current user's obeject
    and send data to the template for display informations.
    """
    tutors = Tutor.objects.get(user=request.user)
    city = tutors.city
    gender = tutors.gender
    expert = tutors.expert

    return render(request, 'profile.html', {
        'user': request.user, 'tutors': tutors, 
        'city': city, 'gender': gender, 
        'expert': expert
    })


def edit_profile(request):
    """ In edit_profile, it will get current user's object.
    and check request type if it's a POST its will check the form that are validated
    and save to the database
    """
    tutors = Tutor.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        tutor_form = EditProfileForm2(request.POST, instance=tutors)
        if form.is_valid():
            form.save()
            tutor_form.save()
            view_profile(request)

            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        tutor_form = EditProfileForm2(instance=tutors)

        return render(request, 'edit_profile.html', {'current_user':tutors,'form': form, 'tutor_form': tutor_form})


def send_match_request(request, tutor_id):
    """ In send_match_request, this method will active when user authenticated.
    we will get user'object which is the id of user that you want to send request
    and create the request that include from_user and to_user. 
    from_user is you and to_user is user who want to sent request.
    """
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=tutor_id)
        frequest, created = Matched_Request.objects.get_or_create(
            from_user=request.user, to_user=user)

        return HttpResponseRedirect('/')


def cancel_match_request(request, tutor_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=tutor_id)
        frequest = Matched_Request.objects.filter(
            from_user=request.user, to_user=user).first()
        frequest.delete()
        return HttpResponseRedirect('/')


def accept_match_request(request, tutor_id):
    from_user = get_object_or_404(User, id=tutor_id)
    frequest = Matched_Request.objects.filter(
        from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.tutor.groupMatch.add(user2.tutor)
    user2.tutor.groupMatch.add(user1.tutor)
    frequest.delete()
    return HttpResponseRedirect('/match-result/')


def delete_match_request(request, tutor_id):
    from_user = get_object_or_404(User, id=tutor_id)
    frequest = Matched_Request.objects.filter(
        from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect('/match-result/')

def unfriend(request,tutor_id):
    current_user = Tutor.objects.get(user=request.user)
    to_unfriend = Tutor.objects.get(pk=tutor_id)
    current_user.groupMatch.remove(to_unfriend)
    return HttpResponseRedirect('/match-result/')

def match_result(request):
    current_user = Tutor.objects.get(user=request.user)
    p = Tutor.objects.get(user=request.user)
    u = p.user

    sent_match_requests = Matched_Request.objects.filter(from_user=p.user)
    rec_match_requests = Matched_Request.objects.filter(to_user=p.user)

    contact = p.groupMatch.all()
    urlroom = {}
    for tutor in contact:
        listuser = []
        name = tutor
        user = tutor.user
        listuser.append(str(user))
        listuser.append(str(u))
        listuser.sort()
        urlroom[name] = listuser[0]+'.'+listuser[1]

    context = {
        'current_user':current_user,
        'u': u,
        'contact_list': contact,
        'sent_match_requests': sent_match_requests,
        'rec_match_requests': rec_match_requests,
        'urlroom': urlroom
    }
    return render(request, "manage_match.html", context)

def review(request, tutor_id):
    tutor = Tutor.objects.get(pk=tutor_id) # Get reviewed_tutor
    reviews = tutor.reviewed_tutor.all() # Get all reviews of tutor
    
    total_point = 0
    if len(reviews) != 0:
        for review in reviews:
            total_point += review.rate
        total_point = float(f'{(total_point / len(reviews)):.2f}')

    if request.method == "POST": # After submit review
        form = ReviewForm(request.POST)
        if form.is_valid():
            reviewer = Tutor.objects.get(user=request.user) # Get Reviewer
            rating_point = request.POST.get('rating','')
            Review.objects.create(comment=form.cleaned_data['comment'],reviewer=reviewer, reviewed_tutor=tutor, rate=rating_point)
            redirect(f'/review/{tutor_id}')
    else: 
        form = ReviewForm() 
    return render(request, "review.html", {"tutor":tutor,"form":form,"reviews":reviews,"range":range(1,6),'total_point':total_point})

def about_group(request):
    if request.user.is_authenticated:
        current_user = Tutor.objects.get(user=request.user)
        return render(request, "about_group.html",{'current_user':current_user})
    
    return render(request, "about_group.html")

def about_app(request):
    if request.user.is_authenticated:
        current_user = Tutor.objects.get(user=request.user)
        return render(request, "about_app.html",{'current_user':current_user})
    return render(request, "about_app.html")

def friend_profile(request,tutor_id):
    tutor = Tutor.objects.get(pk=tutor_id)
    user = tutor.user
    return render(request, 'friend_profile.html', {
        'tutors':tutor, 'user': user , 'city' : tutor.city , 'gender': tutor.gender, 'expert': tutor.expert
    })
    
def help_user(request):
    if request.user.is_authenticated:
        current_user = Tutor.objects.get(user=request.user)
        return render(request, "help.html",{'current_user':current_user})
    return render(request, 'help.html')
        
def answer_user(request, answer_page):
    return render(request, 'answers/answer%s.html' % answer_page)

