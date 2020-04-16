from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tutor(models.Model):
    #In Tutor model , it will store user's information from all user by object
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
    groupMatch = models.ManyToManyField("Tutor", blank=True)

    def __str__(self):
        return self.name
    
    
class MatchedRequest(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

class Review(models.Model):
    reviewer = models.ForeignKey(Tutor, on_delete=models.CASCADE,related_name='reviewer')
    reviewed_tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE,related_name='reviewed_tutor')
    comment = models.TextField(default='',blank=True)
    rate = models.IntegerField(default=1,blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)


