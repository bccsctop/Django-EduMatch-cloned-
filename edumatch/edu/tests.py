from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from edu.views import home_page
from edu.views import register
from edu.views import match_result
from edu.models import Tutor,Matched_Request
from django.contrib.auth.models import User

class HomepageTest(TestCase):

    def test_rootURL_mapping_to_homepageView(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)
    
    def test_rendering_homepageTemplate(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_search_itemInTable_(self):
        ronnie_user = User.objects.create_user('ronnie','ronnie@test.com','ronniepassword')
        helen_user = User.objects.create_user('helen','helen@test.com','helenpassword')
        mark_user = User.objects.create_user('mark','mark@test.com','markpassword')
        Tutor.objects.create(user=helen_user,name='Helen',expert ='Statistic',gender = 'Female',city = 'Ayutthaya')
        Tutor.objects.create(user=ronnie_user,name='Ronnie',expert ='Signal',gender = 'Male',city = 'Bangkok')
        Tutor.objects.create(user=mark_user,name='Mark',expert ='Signal',gender = 'Male',city = 'Bangkok')
        response = self.client.post('/', data={'subject_text': 'Signal','gender_text' : 'Male','city_text' : 'Bangkok'})
        #self.assertNotContains(response,'Helen')
        #self.assertContains(response,'Ronnie')
        

class ListViewTest(TestCase):

    def test_displays_itemInTable(self):
        frankin_user = User.objects.create_user('frankin','frankin@test.com','frankinpassword')
        ronnie_user = User.objects.create_user('ronnie','ronnie@test.com','ronniepassword')

        frankin = Tutor.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = Tutor.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        response = self.client.get(f'/lists/{ronnie.id}')
        self.assertContains(response,'Frankin')
        self.assertNotContains(response,'Ronnie')

    def test_uses_list_template(self):
        frankin_user = User.objects.create_user('frankin','frankin@test.com','frankinpassword')
        frankin = Tutor.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        response = self.client.get(f'/lists/{frankin.id}')
        self.assertTemplateUsed(response, 'list.html')


class RegisterTest(TestCase):

    def test_rootURL_maping_to_homepageVIEW(self):
        found = resolve('/register')
        self.assertEqual(found.func,register)

    
    def test_rendering_registerTemplate(self):
        response = self.client.get('/register')
        self.assertTemplateUsed(response, 'register.html')

    def test_saving_and_verifying_modelItems(self):
        frankin_user = User.objects.create_user('frankin','frankin@test.com','frankinpassword')
        ronnie_user = User.objects.create_user('ronnie','ronnie@test.com','ronniepassword')

        frankin = Tutor.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = Tutor.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        

        saved_tutors = Tutor.objects.all()
        self.assertEqual(saved_tutors.count(),2)

        first_saved_tutor = saved_tutors[0]
        second_saved_tutor = saved_tutors[1]

        self.assertEqual(first_saved_tutor.name,'Frankin')
        self.assertEqual(second_saved_tutor.name,'Ronnie')
        self.assertEqual(first_saved_tutor.gender,second_saved_tutor.gender)
        self.assertEqual(first_saved_tutor.city,second_saved_tutor.city)
        self.assertNotEqual(first_saved_tutor.expert,second_saved_tutor.expert)

class TutorRequestTest(TestCase):

    def test_URL_maping_to_matchResultVIEW(self):
        found = resolve('/match-result/')
        self.assertEqual(found.func,match_result)

    
    def test_rendering_matchResultTemplate(self):
        frankin_user = User.objects.create_user('frankin','frankin@test.com','frankinpassword')
        frankin = Tutor.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.get('/match-result/')
        self.assertTemplateUsed(response, 'manage_match.html')

    def test_sent_and_recieve_request(self):
        frankin_user = User.objects.create_user('frankin','frankin@test.com','frankinpassword')
        ronnie_user = User.objects.create_user('ronnie','ronnie@test.com','ronniepassword')
        betty_user = User.objects.create_user('betty','betty@test.com','bettypassword')
        frankin = Tutor.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = Tutor.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = Tutor.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')
        self.client.login(username='frankin', password='frankinpassword') 
        self.client.get(f'/match-request/send/{ronnie.id}')
        self.client.get(f'/match-request/send/{betty.id}')

        saved_requests = Matched_Request.objects.all()
        self.assertEqual(saved_requests.count(),2)

        first_saved_request = saved_requests[0]
        second_saved_request = saved_requests[1]

        self.assertEqual(first_saved_request.to_user.username,'ronnie')
        self.assertEqual(first_saved_request.from_user.username,'frankin')
        self.assertEqual(second_saved_request.to_user.username,'betty')
        self.assertEqual(second_saved_request.from_user.username,'frankin')

    def test_recieve_and_cancel_request(self):
        frankin_user = User.objects.create_user('frankin','frankin@test.com','frankinpassword')
        ronnie_user = User.objects.create_user('ronnie','ronnie@test.com','ronniepassword')
        betty_user = User.objects.create_user('betty','betty@test.com','bettypassword')
        frankin = Tutor.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = Tutor.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = Tutor.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')

        Matched_Request.objects.create(to_user=ronnie_user,from_user=frankin_user)
        Matched_Request.objects.create(to_user=betty_user,from_user=frankin_user)
        saved_requests = Matched_Request.objects.all()
        self.assertEqual(saved_requests.count(),2)

        self.client.login(username='frankin', password='frankinpassword') 
        self.client.get(f'/match-request/cancel/{ronnie.id}')

        saved_requests = Matched_Request.objects.all()
        self.assertEqual(saved_requests.count(),1)

        first_saved_request = saved_requests[0]

        self.assertEqual(first_saved_request.to_user.username,'betty')
        self.assertEqual(first_saved_request.from_user.username,'frankin')
        

