from django.db import models

class Tutor(models.Model):
    name = models.TextField(default='')