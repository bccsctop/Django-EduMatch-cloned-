from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from edu.models import Tutor

GENDER_CHOICES= [
    ('Male','Male'),
    ('Female', 'Female'),
    ('Neutral', 'Neutral'),
    ]

CITY_CHOICES=[
    ('Bangkok','Bangkok'),('Krabi','Krabi'),('Kanchanaburi','Kanchanaburi'),('Kalasin','Kalasin'),('Kamphaeng','Kamphaeng'),
    ('Khon Kaen','Khon Kaen'),('Chanthaburi','Chanthaburi'),('	Chachoengsao','	Chachoengsao'),('Chonburi','Chonburi'),('Chainat','	Chainat'),('Chaiyaphum','Chaiyaphum'),('Chumphon','Chumphon')
    ,('Chiang Rai','Chiang Rai'),('Chiang Mai','Chiang Mai'),('	Trang','Trang'),('Trat','Trat'),('Tak','Tak'),('Nakhon Nayok','Nakhon Nayok')
    ,('Nakhon Pathom','Nakhon Pathom'),('Nakhon Phanom','Nakhon Phanom'),('Nakhon Ratchasima','Nakhon Ratchasima'),('Nakhon Si Thammarat','Nakhon Si Thammarat'),('Nakhon Sawan','Nakhon Sawan'),('Nonthaburi','Nonthaburi'),('Narathiwat','Narathiwat')
    ,('Nan','Nan'),('Bueng Kan','Bueng Kan'),('Buriram','Buriram'),('Pathum Thani','Pathum Thani'),('Prachuap Khiri Khan','Prachuap Khiri Khan'),('Prachinburi','Prachinburi'),('Pattani','Pattani'),('Ayutthaya','Ayutthaya')
    ,('Phayao','Phayao'),('Phang Nga','Phang Nga'),('Phatthalung','Phatthalung'),('Phichit','Phichit'),('Phitsanulok','Phitsanulok'),('Phetchaburi','Phetchaburi'),('Phetchabun','Phetchabun'),('Phrae','Phrae')
    ,('Phuket','Phuket'),('Maha Sarakham','Maha Sarakham'),('Mukdahan','Mukdahan'),('Mae Hong Son','Mae Hong Son'),('Yasothon','Yasothon'),('Yala','Yala'),('Roi Et','Roi Et'),('Ranong','Ranong')
    ,('Rayong','Rayong'),('Ratchaburi','Ratchaburi'),('Lopburi','Lopburi'),('Lampang','Lampang'),('Lamphun','Lamphun'),('Loei','Loei'),('Sisaket','Sisaket'),('Sakon Nakhon','Sakon Nakhon')
    ,('Songkhla','Songkhla'),('Satun','Satun'),('Samut Prakan','Samut Prakan'),('Samut Songkhram','Samut Songkhram'),('Samut Sakhon','Samut Sakhon'),('Sa Kaeo','Sa Kaeo'),('Saraburi','Saraburi'),('Sing Buri','Sing Buri')
    ,('Sukhothai','Sukhothai'),('Suphan Buri','Suphan Buri'),('Surat Thani','Surat Thani'),('Surin','Surin'),('Nong Khai','Nong Khai'),('Nong Bua Lamphu','Nong Bua Lamphu'),('Ang Thong','Ang Thong'),('Amnat Charoen','Amnat Charoen')
    ,('Udon Thani','Udon Thani'),('Uttaradit','Uttaradit'),('Uthai Thani','Uthai Thani'),('Ubon Ratchathani','Ubon Ratchathani')
]




class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    gender = forms.CharField(max_length=30, required=False, help_text='Optional.',widget=forms.Select(choices=GENDER_CHOICES))
    city = forms.CharField(max_length=30, required=False, help_text='Optional.',widget=forms.Select(choices=CITY_CHOICES))
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
    gender = forms.CharField(max_length=30, required=False, help_text='Optional.',widget=forms.Select(choices=GENDER_CHOICES))
    city = forms.CharField(max_length=30, required=False, help_text='Optional.',widget=forms.Select(choices=CITY_CHOICES))
    expert = forms.CharField(max_length=30, required=False, help_text='Subject that you are expert')
    class Meta:
        model = Tutor
        fields = ('gender', 'city', 'expert')

class ReviewForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':'5','cols':'73'}),label='')
    