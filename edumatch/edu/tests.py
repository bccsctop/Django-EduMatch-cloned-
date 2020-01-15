from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from edu.views import home_page
from edu.views import register
from edu.models import Tutor,Selected_Subject

class HomepageTest(TestCase):

    def test_rootURL_maping_to_homepageVIEW(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)
    
    def test_rendering_homepageTemplate(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_checking_a_POST_request(self):
        self.client.post('/', data={'subject_text': 'A select subject'})
        self.assertEqual(Selected_Subject.objects.count(), 1)
        new_subject = Selected_Subject.objects.first()
        self.assertEqual(new_subject.subject, 'A select subject')
    
    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'subject_text': 'A select subject'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_searching_modelTutor_(self):
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

class RegisterTest(TestCase):

    def test_rootURL_maping_to_homepageVIEW(self):
        found = resolve('/spark/register')
        self.assertEqual(found.func,register)

    
    def test_rendering_homepageTemplate(self):
        response = self.client.get('/spark/register')
        self.assertTemplateUsed(response, 'register.html')

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/spark/register')  

        html = response.content.decode('utf8')  
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Register</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'register.html') 


