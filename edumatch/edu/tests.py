from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from edu.views import home_page
from edu.models import Tutor

class HomepageTest(TestCase):

    def test_rootURL_maping_to_homepageVIEW(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)
    
    def test_rendering_homepageTemplate(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_checking_a_POST_request(self):
        response = self.client.post('/', data={'subject_text': 'A select subject'})
        self.assertIn('A select subject', response.content.decode())

    def test_displays_modelItems_(self):
        Tutor.objects.create(name='Mark')
        Tutor.objects.create(name='Ploy')
        response = self.client.get('/')
        self.assertContains(response,'Mark')
        self.assertContains(response,'Ploy')


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

