from django.urls import resolve,reverse
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from edu.views import home_page
from edu.views import register
from edu.views import friend_profile
from edu.views import view_profile
from edu.views import edit_profile
from edu.forms import EditProfileForm
from edu.forms import EditProfileForm2
from edu.views import match_result
from edu.models import UserAccount,MatchedRequest,Review
from django.contrib.auth.models import User

class HomepageTest(TestCase):

    def test_rootURL_mapping_to_homepageView(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)
    
    def test_rendering_homepageTemplate(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_search_itemInTable_(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        betty_user = User.objects.create_user(username='betty',email='betty@test.com',password='bettypassword',first_name='Betty',last_name='Caesar')
        henderson_user = User.objects.create_user(username='henderson',email='henderson@test.com',password='hendersonpassword',first_name='Henderson',last_name='Dabney')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = UserAccount.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')
        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.post('/', data={'subject_text': 'Signal','gender_text' : 'Male','city_text' : 'Bangkok'})
        self.assertNotContains(response,'Betty')
        self.assertContains(response,'Ronnie')
        


class TutorRequestTest(TestCase):

    def test_URL_maping_to_matchResultVIEW(self):
        found = resolve('/match-result/')
        self.assertEqual(found.func,match_result)

    
    def test_rendering_matchResultTemplate(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.get('/match-result/')
        self.assertTemplateUsed(response, 'manage_match.html')

    def test_sent_and_recieve_request(self):
        
        #Create three user that have thier own characteristic. 
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        betty_user = User.objects.create_user(username='betty',email='betty@test.com',password='bettypassword',first_name='Betty',last_name='Caesar')
        henderson_user = User.objects.create_user(username='henderson',email='henderson@test.com',password='hendersonpassword',first_name='Henderson',last_name='Dabney')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = UserAccount.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')
        
        #Login as Frankin (Require User Authentication)
        self.client.login(username='frankin', password='frankinpassword') 
        
        #Send request to Ronnie and Betty
        self.client.get(f'/match-request/send/{ronnie.id}')
        self.client.get(f'/match-request/send/{betty.id}')

        #Check size of request that have been send
        saved_requests = MatchedRequest.objects.all()
        self.assertEqual(saved_requests.count(),2)

        #Seperate each request
        first_saved_request = saved_requests[0]
        second_saved_request = saved_requests[1]

        #Check that sender and reciever are right person
        self.assertEqual(first_saved_request.to_user.username,'ronnie')
        self.assertEqual(first_saved_request.from_user.username,'frankin')
        self.assertEqual(second_saved_request.to_user.username,'betty')
        self.assertEqual(second_saved_request.from_user.username,'frankin')

    def test_send_and_cancel_request(self):
        #Create three user that have thier own characteristic. 
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        betty_user = User.objects.create_user(username='betty',email='betty@test.com',password='bettypassword',first_name='Betty',last_name='Caesar')
        henderson_user = User.objects.create_user(username='henderson',email='henderson@test.com',password='hendersonpassword',first_name='Henderson',last_name='Dabney')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = UserAccount.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')

        #Create a request to Ronnie and Betty
        MatchedRequest.objects.create(to_user=ronnie_user,from_user=frankin_user)
        MatchedRequest.objects.create(to_user=betty_user,from_user=frankin_user)
        
        #Check size of request that have send
        saved_requests = MatchedRequest.objects.all()
        self.assertEqual(saved_requests.count(),2)

        #Login as Frankin (Require User Authentication)
        self.client.login(username='frankin', password='frankinpassword') 
        
        #Cancel a request of Ronnie
        self.client.get(f'/match-request/cancel/{ronnie.id}')

        #Check size of request that have been cancel
        saved_requests = MatchedRequest.objects.all()
        self.assertEqual(saved_requests.count(),1)

        #Seperate each request
        first_saved_request = saved_requests[0]

        #Check that remain sender and reciever are right person
        self.assertEqual(first_saved_request.to_user.username,'betty')
        self.assertEqual(first_saved_request.from_user.username,'frankin')
        

    def test_recieve_and_accept_request(self):
        #Create three user that have thier own characteristic. 
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        betty_user = User.objects.create_user(username='betty',email='betty@test.com',password='bettypassword',first_name='Betty',last_name='Caesar')
        henderson_user = User.objects.create_user(username='henderson',email='henderson@test.com',password='hendersonpassword',first_name='Henderson',last_name='Dabney')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = UserAccount.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')

        #Create a request from Ronnie and Betty
        MatchedRequest.objects.create(to_user=frankin_user,from_user=ronnie_user)
        MatchedRequest.objects.create(to_user=frankin_user,from_user=betty_user)
        
        #Check size of request that have been send
        saved_requests = MatchedRequest.objects.all()
        self.assertEqual(saved_requests.count(),2)

        #Login as Frankin (Require User Authentication)
        self.client.login(username='frankin', password='frankinpassword') 
        
        #Accept a request from Ronnie
        self.client.get(f'/match-request/accept/{ronnie.id}')

        #Check size of request that remain
        saved_requests = MatchedRequest.objects.all()
        self.assertEqual(saved_requests.count(),1)

        #Check that remain sender and reciever are right person
        frankin_tutors = frankin.groupMatch.all()
        self.assertEqual(frankin_tutors.count(),1)

        #Check that remain sender and reciever are right person
        first_frankin_tutor = frankin_tutors[0]
        self.assertEqual(first_frankin_tutor.name,'Ronnie')

    def test_recieve_and_reject_request(self):
        #Create three user that have thier own characteristic. 
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        betty_user = User.objects.create_user(username='betty',email='betty@test.com',password='bettypassword',first_name='Betty',last_name='Caesar')
        henderson_user = User.objects.create_user(username='henderson',email='henderson@test.com',password='hendersonpassword',first_name='Henderson',last_name='Dabney')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = UserAccount.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')

        #Create a request from Ronnie and Betty
        MatchedRequest.objects.create(to_user=frankin_user,from_user=ronnie_user)
        MatchedRequest.objects.create(to_user=frankin_user,from_user=betty_user)
        
        #Check size of request that have been send
        saved_requests = MatchedRequest.objects.all()
        self.assertEqual(saved_requests.count(),2)

        #Login as Frankin (Require User Authentication)
        self.client.login(username='frankin', password='frankinpassword') 
        
        #Reject a request from Ronnie
        self.client.get(f'/match-request/reject/{ronnie.id}')

        #Check size of request that remain
        saved_requests = MatchedRequest.objects.all()
        self.assertEqual(saved_requests.count(),1)

        #Check that remain sender and reciever are right person
        frankin_tutors = frankin.students.all()
        self.assertEqual(frankin_tutors.count(),0)

    def test_recieve_and_accept_request(self):
        #Create three user that have thier own characteristic. 
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        betty_user = User.objects.create_user(username='betty',email='betty@test.com',password='bettypassword',first_name='Betty',last_name='Caesar')
        henderson_user = User.objects.create_user(username='henderson',email='henderson@test.com',password='hendersonpassword',first_name='Henderson',last_name='Dabney')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = UserAccount.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')

        #Create a request from Ronnie and Betty
        MatchedRequest.objects.create(to_user=frankin_user,from_user=ronnie_user)
        MatchedRequest.objects.create(to_user=frankin_user,from_user=betty_user)
        
        #Check size of request that have been send
        saved_requests = MatchedRequest.objects.all()
        self.assertEqual(saved_requests.count(),2)

        #Login as Frankin (Require User Authentication)
        self.client.login(username='frankin', password='frankinpassword') 
        
        #Accept a request from Ronnie
        response = self.client.get('/match-result/')

        #Check that remain sender and reciever are right person
        self.assertContains(response,'Ronnie  Bacham')
        self.assertContains(response,'Betty  Caesar')

class ProfileTest(TestCase):
    def test_URL_maping_to_PorfileVIEW(self):
        found = resolve('/profile')
        self.assertEqual(found.func,view_profile)

    def test_rendering_ProfileTemplate(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.get('/profile')
        self.assertTemplateUsed(response, 'profile.html')

    def test_show_Profile(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        betty_user = User.objects.create_user(username='betty',email='betty@test.com',password='bettypassword',first_name='Betty',last_name='Caesar')
        henderson_user = User.objects.create_user(username='henderson',email='henderson@test.com',password='hendersonpassword',first_name='Henderson',last_name='Dabney')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = UserAccount.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')
        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.post('/profile')
        self.assertContains(response,'frankin')
        self.assertContains(response,'Male')
        self.assertContains(response,'Bangkok')
        self.assertContains(response,'Statistic')
        self.assertNotContains(response,'Betty')
        self.assertNotContains(response,'Ronnie')

    def test_URL_maping_to_PorfileEditVIEW(self):
        found = resolve('/profile/edit')
        self.assertEqual(found.func,edit_profile)

    def test_rendering_ProfileEditTemplate(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.get('/profile/edit')
        self.assertTemplateUsed(response, 'edit_profile.html')

    def test_edit_forms(self):
        form1_data = {'username': 'Betty','first_name' : 'Betty', 'last_name':'King'}
        form1 = EditProfileForm(data=form1_data)
        self.assertTrue(form1.is_valid())
        form2_data = {'gender':'Female', 'city':'Bangkok', 'expert':'Signal'}
        form2 = EditProfileForm2(data=form2_data)
        self.assertTrue(form2.is_valid())
        
    def test_URL_maping_to_FriendPorfileVIEW(self):
        found = resolve('/friendprofile/0')
        self.assertEqual(found.func,friend_profile)

    def test_rendering_FriendProfileTemplate(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.get(f'/friendprofile/{ronnie.id}')
        self.assertTemplateUsed(response, 'friend_profile.html')

    def test_view_friend_profile(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.get(f'/friendprofile/{ronnie.id}')
        self.assertContains(response,'ronnie')
        self.assertContains(response,'Male')
        self.assertContains(response,'Bangkok')
        self.assertContains(response,'Signal')
        self.assertNotContains(response,'Betty')
        self.assertNotContains(response,'frankin')

class ReviewTest(TestCase):
    def test_URL_maping_to_review(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        found = resolve(f'/review/{frankin.id}')
        self.assertEqual(found.url_name,'review')

    
    def test_rendering_ReviewTemplate(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.get(f'/review/{ronnie.id}')
        self.assertTemplateUsed(response, 'review.html')
    
    def test_after_POST_pass_correct_review_to_template(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        betty_user = User.objects.create_user(username='betty',email='betty@test.com',password='bettypassword',first_name='Betty',last_name='Caesar')
        henderson_user = User.objects.create_user(username='henderson',email='henderson@test.com',password='hendersonpassword',first_name='Henderson',last_name='Dabney')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = UserAccount.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')

        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.post(reverse('review',args=[ronnie.id]),{'comment':'ronnie is very good','rating':5}, follow=True)

        self.assertEqual(response.context['reviews'][0].comment,'ronnie is very good')
        self.assertEqual(response.context['reviews'][0].rate,5)
        self.assertEqual(response.context['reviews'][0].reviewer,frankin)
        self.assertEqual(response.context['reviews'][0].reviewed_tutor,ronnie)

        self.client.login(username='betty', password='bettypassword') 
        response = self.client.post(reverse('review',args=[ronnie.id]),{'comment':'ronnie is the best','rating':4}, follow=True)

        self.assertEqual(response.context['reviews'][1].comment,'ronnie is the best')
        self.assertEqual(response.context['reviews'][1].rate,4)
        self.assertEqual(response.context['reviews'][1].reviewer,betty)
        self.assertEqual(response.context['reviews'][1].reviewed_tutor,ronnie)

    def test_after_POST__review_template_show_review(self):
        frankin_user = User.objects.create_user(username='frankin',email='frankin@test.com',password='frankinpassword',first_name='Frankin',last_name='Alibaba')
        ronnie_user = User.objects.create_user(username='ronnie',email='ronnie@test.com',password='ronniepassword',first_name='Ronnie',last_name='Bacham')
        betty_user = User.objects.create_user(username='betty',email='betty@test.com',password='bettypassword',first_name='Betty',last_name='Caesar')
        henderson_user = User.objects.create_user(username='henderson',email='henderson@test.com',password='hendersonpassword',first_name='Henderson',last_name='Dabney')
        frankin = UserAccount.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = UserAccount.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = UserAccount.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')

        self.client.login(username='frankin', password='frankinpassword') 
        response = self.client.post(reverse('review',args=[ronnie.id]),{'comment':'ronnie is very good','rating':5}, follow=True)

        self.assertContains(response,'Frankin')
        self.assertContains(response,'ronnie is very good')

        self.client.login(username='betty', password='bettypassword') 
        response = self.client.post(reverse('review',args=[ronnie.id]),{'comment':'ronnie is the best','rating':4}, follow=True)

        self.assertContains(response,'Frankin')
        self.assertContains(response,'ronnie is very good')
        self.assertContains(response,'Betty')
        self.assertContains(response,'ronnie is the best')