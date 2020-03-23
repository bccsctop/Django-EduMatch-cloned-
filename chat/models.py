from django.db import models


class Chatroom_message(models.Model):
    room_name = models.TextField(blank=True)
    author = models.TextField(blank=True)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.room_name



