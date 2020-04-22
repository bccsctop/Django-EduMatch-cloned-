from django.contrib import admin
from chat.models import Chatroom_message
from edu.models import MatchedRequest,UserAccount,Review

admin.site.register(UserAccount)
admin.site.register(MatchedRequest)
admin.site.register(Chatroom_message)
admin.site.register(Review)