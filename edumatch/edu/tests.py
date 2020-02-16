from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from edu.views import home_page
from edu.views import register
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

    
    def test_rendering_homepageTemplate(self):
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
