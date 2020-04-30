from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse
from edu.models import UserAccount, MatchedRequest, Review
from edu.forms import SignUpForm, EditProfileForm, EditProfileForm2, ReviewForm, CITY_CHOICES
import time
import datetime


def home_page(request):
    if not request.user.is_authenticated:  #Check that user is logged in.
        return redirect('login')           #If user is not logged in to the server page will redirect to login page

    users = UserAccount.objects.all()                     #Get Tutor object and store in tutors variable
    subject = request.POST.get('subject_text', '')   #Get subject_text in the search box and store in subject variable
    gender = request.POST.get('gender_text', '')     #Get gender_text at dropdown and store in gender variable
    city = request.POST.get('city_text', '')         #Get city_text at dropdown and store in city variable

    cities = [i[0] for i in CITY_CHOICES]                                   #Store CITY_CHOICES that are declare in form.py to cities variable
    users = users.filter(expert=subject) if subject != '' else users     #If subject is existed tutors will filter user that in condition.
    users = users.filter(gender=gender) if gender != '' else users       #If gender is existed tutors will filter user that in condition.
    users = users.filter(city=city) if city != '' else users             #If city is existed tutors will filter user that in condition.
    users = users.exclude(user=request.user)                              #Remove current user out of tutors
    current_user = UserAccount.objects.get(user=request.user)                     #Get current user and store to current_user variable

    for match_user in current_user.tutors.all():                                    #Remove the user that already match with current user
        users = users.exclude(pk=match_user.id)
    for match_user in current_user.students.all():                                  
        users = users.exclude(pk=match_user.id)

    recieve_match_requests = MatchedRequest.objects.filter(to_user=current_user.user)   #Filter the MatchRequest that current user recieved
    sent_match_requests = MatchedRequest.objects.filter(from_user=current_user.user)    #Filter the MatchRequest that current user sent to another user
    
    requested_users = []            #already sent request
    unrequest_users = []          #not send request yet
    for i in users:                                #Check the user that curent user already sent the request
        numCount = 0
        for j in sent_match_requests:
            if i.name == j.to_user.first_name:
                requested_users.append(i)          #current user already sent the request 
                numCount+=1
        if numCount == 0:
            unrequest_users.append(i)              #current user never send the request

    if len(recieve_match_requests) > 0 :                #If current user have recieved request
        return render(request, 'home.html', {
                'requested_users': requested_users,
                'unrequest_users': unrequest_users,
                'amount_recieve': len(recieve_match_requests),
                'current_user': current_user,
                'cites':cities
            })

    return render(request, 'home.html', {           #If current user not have recieved request
        'requested_users': requested_users,
        'unrequest_users': unrequest_users,
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
            #Save data to database / register successful
            user = form.save()
            user.refresh_from_db()
            user.save()
            #Get password from form and store in password
            password = form.cleaned_data.get('password1')
            #Test login 
            user = authenticate(username=user.username, password=password)
            login(request, user)
            #Create use object
            user = UserAccount.objects.create(user=user, 
                                        name=form.cleaned_data['first_name'], gender=form.cleaned_data['gender'], 
                                        city=form.cleaned_data['city'], expert=form.cleaned_data['subject'])

            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def view_profile(request):
    """ In view_profile, it will get current user's object
    and send data to the template for display informations.
    """
    users = UserAccount.objects.get(user=request.user)
    city = users.city
    gender = users.gender
    expert = users.expert

    return render(request, 'profile.html', {
        'user': request.user, 'users': users, 
        'city': city, 'gender': gender, 
        'expert': expert
    })


def edit_profile(request):
    """ In edit_profile, it will get current user's object.
    and check request type if it's a POST it will check the form that are validated
    and save to the database
    """
    users = UserAccount.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        tutor_form = EditProfileForm2(request.POST, instance=users)
        if form.is_valid():
            #Save firstname, lastname, username
            form.save()
            #Save gender, city, expert
            tutor_form.save()

            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        tutor_form = EditProfileForm2(instance=users)

        return render(request, 'edit_profile.html', {'current_user':users,'form': form, 'tutor_form': tutor_form})


def send_match_request(request, tutor_id):
    """ In send_match_request, this method will active when user authenticated.
    we will get user'object which can select by id of user that you want to send request
    and create the request that include from_user and to_user. 
    from_user is you and to_user is user who you want to sent request to.
    """
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=tutor_id)
        request, created = MatchedRequest.objects.get_or_create(
            from_user=request.user, to_user=user)

        return HttpResponseRedirect('/')


def cancel_match_request(request, tutor_id):
    """ In cancel_match_request, this method will active when user authenticated.
    we will get user'object which can select by id of user that you want to cancel request
    and filter the Match_Request by your username and username of user that you send 
    the request and delete the request.
    """
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=tutor_id)
        request = MatchedRequest.objects.filter(
            from_user=request.user, to_user=user).first()
        #Delete request
        request.delete()

        return HttpResponseRedirect('/')


def accept_match_request(request, tutor_id):
    #In accept_match_request, we will get user'object which can select by id of user that you want to accept request.
    from_user = get_object_or_404(User, id=tutor_id)
    #Filter Match_Request and store the request to frequest
    request = MatchedRequest.objects.filter(
        from_user=from_user, to_user=request.user).first()  
    user1 = request.to_user
    user2 = from_user
    #Add user match to both of user
    user1.useraccount.students.add(user2.useraccount)
    user2.useraccount.tutors.add(user1.useraccount)
    request.delete()   #delete request
    
    return HttpResponseRedirect('/match-result/')


def reject_match_request(request, tutor_id):
    #In reject_match_request, we will get user'object which can select by id of user that you want to delete request.
    from_user = get_object_or_404(User, id=tutor_id)
    #Filter Match_Request and store the request to frequest
    request = MatchedRequest.objects.filter(
        from_user=from_user, to_user=request.user).first()
    #delete frequest
    request.delete()

    return HttpResponseRedirect('/match-result/')

def unfriend(request,tutor_id):
    #Get current user's object
    current_user = UserAccount.objects.get(user=request.user)
    #Get user who want to unfriend 
    to_unfriend = UserAccount.objects.get(pk=tutor_id)
    #Remove relations/delete to_unfriend out of friend list
    if to_unfriend in current_user.tutors.all():
        current_user.tutors.remove(to_unfriend)
        to_unfriend.students.remove(current_user)
        return HttpResponseRedirect('/match-result/')
    if to_unfriend in current_user.students.all():
        current_user.students.remove(to_unfriend)
        to_unfriend.tutors.remove(current_user)
        return HttpResponseRedirect('/match-result/')
    

def match_result(request):
    #Get current user's object
    current_user = UserAccount.objects.get(user=request.user)
    #Get current user's username
    current_username = current_user.user
    #Filter Match_Request that belong to current user
    sent_match_requests = MatchedRequest.objects.filter(from_user=current_user.user)
    recieve_match_requests = MatchedRequest.objects.filter(to_user=current_user.user)
    #Get all user that current user are matched
    tutor_contact = current_user.tutors.all()
    student_contact = current_user.students.all()
    #Create room's name for chatting by using both username, sorting and use "." to seperate two names
    tutor_chatroom = {}
    student_chatroom = {}
    for tutor in tutor_contact:
        list_user = []
        name = tutor
        another_user = tutor.user
        list_user.append(str(another_user))
        list_user.append(str(current_username)) 
        list_user.sort()
        tutor_chatroom[name] = list_user[0]+'.'+list_user[1]
    for student in student_contact:
        list_user = []
        name = student
        another_user = student.user
        list_user.append(str(another_user))
        list_user.append(str(current_username))
        list_user.sort()
        student_chatroom[name] = list_user[0]+'.'+list_user[1]
    #Context that will be send to template
    context = {
        'current_user':current_user,
        'current_username': current_username,
        'tutor_contact': tutor_contact,
        'student_contact': student_contact,
        'sent_match_requests': sent_match_requests,
        'recieve_match_requests': recieve_match_requests,
        'tutor_chatroom': tutor_chatroom,
        'student_chatroom': student_chatroom
    }

    return render(request, "manage_match.html", context)

def review(request, tutor_id):
    tutor_user = UserAccount.objects.get(pk=tutor_id) # Get user's object that current user want to review
    reviews = tutor_user.reviewed_tutor.all() # Get all reviews's tutor
    #Find average score
    total_point = 0
    if len(reviews) != 0:
        for review in reviews:
            total_point += review.rate
        total_point = float(f'{(total_point / len(reviews)):.2f}')
    # When submit review
    if request.method == "POST": 
        form = ReviewForm(request.POST)
        if form.is_valid():
            reviewer = UserAccount.objects.get(user=request.user) # Get Reviewer/current user object
            rating_point = request.POST.get('rating','')    #Get rating_point
            #Create new review
            Review.objects.create(comment=form.cleaned_data['comment'],reviewer=reviewer, reviewed_tutor=tutor_user, rate=rating_point)
            return HttpResponseRedirect(reverse('review',args=(tutor_id,)))
    else: 
        form = ReviewForm()

    return render(request, "review.html", {
        "tutor_user":tutor_user, "form":form, 
        "reviews":reviews, "range":range(1,6),
        "total_point":total_point})

def remove_review(request, review_id, tutor_id):
    review = get_object_or_404(Review, id=review_id)
    reviewer = review.reviewer
    if  request.user.is_authenticated and \
        request.user == reviewer.user and \
        request.method == "POST" :
            review.delete()
            
    return HttpResponseRedirect(f'/review/{tutor_id}')

def about_group(request):
    #In about_group, this method just send user's object to template for review button
    if request.user.is_authenticated:
        current_user = UserAccount.objects.get(user=request.user)
        return render(request, "about_group.html",{'current_user':current_user})
    
    return render(request, "about_group.html")

def about_app(request):
    #In about_app, this method just send user's object to template for review button
    if request.user.is_authenticated:
        current_user = UserAccount.objects.get(user=request.user)
        return render(request, "about_app.html",{'current_user':current_user})
    return render(request, "about_app.html")

def friend_profile(request,tutor_id):
    #Get friend's object and fetch information and store in variable
    friend_user = UserAccount.objects.get(pk=tutor_id)
    user = friend_user.user
    city = friend_user.city
    gender = friend_user.gender
    expert = friend_user.expert

    return render(request, 'friend_profile.html', {
        'friend_user':friend_user, 'user': user,
        'city' : city, 'gender': gender, 
        'expert': expert
    })
    
def help_user(request):
    #In help_user, this method just send user's object to template for review button
    if request.user.is_authenticated:
        current_user = UserAccount.objects.get(user=request.user)
        return render(request, "help.html",{'current_user':current_user})
        
    return render(request, 'help.html')
        
def answer_user(request, answer_page):
    #Redirect to each answer page
    return render(request, 'answers/answer%s.html' % answer_page)

