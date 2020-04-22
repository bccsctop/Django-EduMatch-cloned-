from django.shortcuts import render
from .models import Chatroom_message
from edu.models import UserAccount


def chat_room(request, room_name):
    #Get current user's object
    current_user = UserAccount.objects.get(user=request.user)
    #Get room name
    room_name = str(room_name)
    #Ger chat log
    chat_log = ""
    if Chatroom_message.objects.filter(room_name=room_name).exists() :
       chat_log = Chatroom_message.objects.get(room_name=room_name).message

    return render(request, 'chat/room.html', {
        'room_name': room_name ,
        'chat_log' : chat_log,
        'current_user': current_user,
    })
