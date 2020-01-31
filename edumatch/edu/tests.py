from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from edu.views import home_page
from edu.views import register
from edu.models import Tutor,Selected_Subject

class HomepageTest(TestCase):

    def test_rootURL_mapping_to_homepageView(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)
    
    def test_rendering_homepageTemplate(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_display_itemInTable_(self):
        Tutor.objects.create(name='Frankin',expert ='Statistic')
        Tutor.objects.create(name='Ronnie',expert ='Signal')
        response = self.client.get('/')
        self.assertContains(response,'Frankin')
        self.assertContains(response,'Ronnie')
        

class ListViewTest(TestCase):

    def test_displays_itemInTable(self):
        frankin = Tutor.objects.create(name='Frankin',expert ='Statistic')
        ronnie = Tutor.objects.create(name='Ronnie',expert ='Signal')
        response = self.client.get(f'/lists/{ronnie.id}')
        self.assertContains(response,'Frankin')
        self.assertNotContains(response,'Ronnie')

    def test_uses_list_template(self):
        frankin = Tutor.objects.create(name='Frankin',expert ='Statistic')
        response = self.client.get(f'/lists/{frankin.id}')
        self.assertTemplateUsed(response, 'list.html')

class TutorModelTest(TestCase):
    
    def test_saving_and_verifying_modelItems(self):
        first_tutor = Tutor()
        first_tutor.name = 'Mark'
        first_tutor.save()

        second_tutor = Tutor()
        second_tutor.name = 'Ploy'
        second_tutor.save()

        saved_tutors = Tutor.objects.all()
        self.assertEqual(saved_tutors.count(),2)

        first_saved_tutor = saved_tutors[0]
        second_saved_tutor = saved_tutors[1]

        self.assertEqual(first_saved_tutor.name,'Mark')
        self.assertEqual(second_saved_tutor.name,'Ploy')

class RegisterTest(TestCase):

    def test_rootURL_maping_to_homepageVIEW(self):
        found = resolve('/register')
        self.assertEqual(found.func,register)

    
    def test_rendering_homepageTemplate(self):
        response = self.client.get('/register')
        self.assertTemplateUsed(response, 'register.html')


