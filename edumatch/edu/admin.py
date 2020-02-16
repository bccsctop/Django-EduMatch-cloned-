from django.contrib import admin
from chat.models import Chatroom_message
from .models import Matched_Request,Tutor

admin.site.register(Tutor)
admin.site.register(Matched_Request)
admin.site.register(Chatroom_message)