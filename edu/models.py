from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserAccount(models.Model):
    #In UserAccount model , it will store user's information from all user by object
    #It store user information such as 
    #user -> username, password
    user = models.OneToOneField(User, on_delete=models.CASCADE ,default=None)
    #name -> firstname
    name = models.TextField(default='',blank=True)
    #gender can be = Male, Female, Neutral
    gender = models.TextField(default='',blank=True)
    #city can be all of CITY_CHOICES in form.py
    city = models.TextField(default='',blank=True)
    #expert -> subject that each user expert
    expert = models.TextField(default='',blank=True)
    #Store relations between this user to others user who are matched
    tutors = models.ManyToManyField("UserAccount", blank=True, related_name='list_of_tutor')
    students = models.ManyToManyField("UserAccount", blank=True, related_name='list_of_student')

    #when you in admin site you can see each object with the name by this function
    def __str__(self):
        return self.name
    
    
class MatchedRequest(models.Model):
    #In MatchRequest , it is for store request.
    #When each user send the request to another user for being a tutor
    #to_user = this request send to who
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user')
    #from_user = who send this request
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user')
    #Fetch time
    timestamp = models.DateTimeField(auto_now_add=True)
    
    #when you in admin site you can see each object with this format "From (from_user), to (to_user)" by this function
    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

class Review(models.Model):
    #In Review , it will store point that each other user voted
    #reviewer store who are review this tutor
    reviewer = models.ForeignKey(UserAccount, on_delete=models.CASCADE,related_name='reviewer')
    #reviewed_tutor store tutor that be reviewed
    reviewed_tutor = models.ForeignKey(UserAccount, on_delete=models.CASCADE,related_name='reviewed_tutor')
    #comment store message that explain to this tutor
    comment = models.TextField(default='',blank=True)
    #rate store point that be reviewed
    rate = models.IntegerField(default=1,blank=True)
    #date store when this review happend
    date = models.DateTimeField(auto_now_add=True, blank=True)


