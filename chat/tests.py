from django.test import TestCase
from chat.views import room
from django.urls import resolve



class ChatTests(TestCase):
    

    def test_rootURL_mapping_to_ChatRoom(self):
        
        found = resolve('/chat/betty.frankin/')
        self.assertEqual(found.func,room)

    def test_rendering_chatTemplate(self):

        #Login as Frankin (Require User Authentication)
        self.client.login(username='frankin', password='frankinpassword') 

        #Check template used ,user that loged in and room name when access chat room
        response = self.client.get('/chat/betty.frankin/')
        self.assertTemplateUsed(response, 'chat/room.html')
        self.assertContains(response,'frankin') #user log in now
        self.assertContains(response,'betty.frankin') #room name
