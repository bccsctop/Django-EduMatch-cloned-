from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from edu.views import home_page
from edu.models import Tutor

class HomepageTest(TestCase):

    def test_root_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)
    
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class TutorModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
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
