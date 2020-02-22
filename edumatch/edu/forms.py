from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from edu.models import Tutor,Matched_Request



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    gender = forms.CharField(max_length=30, required=False, help_text='Optional.')
    city = forms.CharField(max_length=30, required=False, help_text='Optional.')
    subject = forms.CharField(max_length=30, required=False, help_text='Subject that you are expert')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'gender', 'city', 'subject', 'password1', 'password2', )


class EditProfileForm(UserChangeForm):
    password = None
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
class EditProfileForm2(ModelForm):
    gender = forms.CharField(max_length=30, required=False, help_text='Optional.')
    city = forms.CharField(max_length=30, required=False, help_text='Optional.')
    expert = forms.CharField(max_length=30, required=False, help_text='Subject that you are expert')
    class Meta:
        model = Tutor
        fields = ('gender', 'city', 'expert')

class ReviewForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    