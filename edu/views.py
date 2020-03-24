from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from edu.models import Tutor, Matched_Request, Review
from edu.forms import SignUpForm, EditProfileForm, EditProfileForm2, ReviewForm
# Create your views here.


def home_page(request):

    tutors = Tutor.objects.all()
    
    subject = request.POST.get('subject_text', '')
    gender = request.POST.get('gender_text', '')
    city = request.POST.get('city_text', '')

    tutors = tutors.filter(expert=subject) if subject != '' else tutors
    tutors = tutors.filter(gender=gender) if gender != '' else tutors
    tutors = tutors.filter(city=city) if city != '' else tutors
    tutors = tutors.exclude(
        user=request.user) if request.user.is_authenticated else tutors
        
    if request.user.is_authenticated:
        tutors = tutors.exclude(user=request.user)
        p = Tutor.objects.get(user=request.user)
        rec_match_requests = Matched_Request.objects.filter(to_user=p.user)
        if len(rec_match_requests) > 0 :
            return render(request, 'home.html', {
                'tutors': tutors,
                'amountRecieve': len(rec_match_requests)
            })

    return render(request, 'home.html', {
        'tutors': tutors
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

            tutor = Tutor.objects.create(user=user, name=form.cleaned_data['first_name'], gender=form.cleaned_data[
                                         'gender'], city=form.cleaned_data['city'], expert=form.cleaned_data['subject'])

            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def view_profile(request):
    tutors = Tutor.objects.get(user=request.user)
    #test = Tutor.objects.get(user = request.user)
    return render(request, 'profile.html', {
        'user': request.user, 'tutors': tutors, 'city': tutors.city, 'gender': tutors.gender, 'expert': tutors.expert
    })


def edit_profile(request):
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
        return render(request, 'edit_profile.html', {'form': form, 'tutor_form': tutor_form})


def send_match_request(request, tutor_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=tutor_id)
        matchUser = Tutor.objects.get(user=user)
        matchUser.isMatched = 'True'
        matchUser.save()
        frequest, created = Matched_Request.objects.get_or_create(
            from_user=request.user, to_user=user)
        return HttpResponseRedirect('/')


def cancel_match_request(request, tutor_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=tutor_id)
        matchUser = Tutor.objects.get(user=user)
        matchUser.isMatched = 'False'
        matchUser.save()
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


def match_result(request):
    
    p = Tutor.objects.get(user=request.user)
    u = p.user

    sent_match_requests = Matched_Request.objects.filter(from_user=p.user)
    rec_match_requests = Matched_Request.objects.filter(to_user=p.user)

    contact = p.groupMatch.all()
    urlroom = {}
    for i in contact:
        listuser = []
        name = i.user
        listuser.append(str(name))
        listuser.append(str(u))
        listuser.sort()
        urlroom[name] = listuser[0]+'.'+listuser[1]

    context = {
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
    if request.method == "POST": # After submit review
        form = ReviewForm(request.POST)
        if form.is_valid():
            reviewer = Tutor.objects.get(user=request.user) # Get Reviewer
            Review.objects.create(comment=form.cleaned_data['comment'],reviewer=reviewer, reviewed_tutor=tutor)
            redirect(f'/review/{tutor_id}')
    else: 
        form = ReviewForm()
    return render(request, "review.html", {"tutor":tutor,"form":form,"reviews":reviews})

def about_group(request):
    return render(request, "about_group.html")

def about_app(request):
    return render(request, "about_app.html")

def friend_profile(request, tutor_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=tutor_id)
        p = Tutor.objects.get(user=request.user)
        u = p.user
        contact = p.groupMatch.all()
        urlroom = {}


