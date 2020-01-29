from django.db import models

class Tutor(models.Model):
    name = models.TextField(default='')
    expert = models.TextField(default='')
    
class Selected_Subject(models.Model):
    subject = models.TextField(default='')