from django.contrib import admin

from .models import Matched_Request,Tutor

admin.site.register(Tutor)
admin.site.register(Matched_Request)