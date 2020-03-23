from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from selenium.webdriver.support.ui import Select
import time
import unittest
from edu.models import Tutor

class ReviewTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

        # Create a database for testing
        frankin_user = User.objects.create_user(
            'frankin', 'frankin@test.com', 'frankinpassword')
        ronnie_user = User.objects.create_user(
            'ronnie', 'ronnie@test.com', 'ronniepassword')
        betty_user = User.objects.create_user(
            'betty', 'betty@test.com', 'bettypassword')
        henderson_user = User.objects.create_user(
            'henderson', 'henderson@test.com', 'hendersonpassword')
        frankin = Tutor.objects.create(
            user=frankin_user, name='Frankin', gender='Male', city='Bangkok', expert='Statistic')
        ronnie = Tutor.objects.create(
            user=ronnie_user, name='Ronnie', gender='Male', city='Bangkok', expert='Signal')
        betty = Tutor.objects.create(
            user=betty_user, name='Betty', gender='Female', city='Bangkok', expert='Signal')
        henderson = Tutor.objects.create(
            user=henderson_user, name='Henderson', gender='Male', city='Chiangmai', expert='Signal')

    def tearDown(self):
        self.browser.quit()

    def login(self, username, password):

        # He is going to login , So He click on login
        login = self.browser.find_element_by_id('login')
        login.send_keys(Keys.ENTER)
        time.sleep(5)

        # He see textbox with "Username".So he enter username
        # He types his usernanme nto a text box
        username_box = self.browser.find_element_by_id('id_username')
        username_box.send_keys(username)

        # He see textbox with "Password".So he enter password
        # He types his password into a text box
        password1_box = self.browser.find_element_by_id('id_password')
        password1_box.send_keys(password)

        # He click on a Sign_in button.
        sign_in_button = self.browser.find_element_by_id('sign_in')
        sign_in_button.send_keys(Keys.ENTER)
        time.sleep(5)

    def test_user_can_review_a_tutor(self):

        # Ronnie is a student of Frankin
        # He study with him for 2 weeks
        # So He want to review his tutor
        # Then He go to spark website

        self.browser.get(self.live_server_url)

        # Ronnie login to spark website
        # ? self.login is login function for refactoring code
        self.login('ronnie', 'ronniepassword')

        # Ronnie is going to review his tutor
        frankin = Tutor.objects.get(name='Frankin')
        self.browser.get(f'{self.live_server_url}/review/{frankin.id}')
        time.sleep(5)

        # He see Review in header of website
        header = self.browser.find_element_by_id('review-header').text
        self.assertEqual('Review', header)

        # Ronnie see the comment box
        # So he type 'Frankin is very good Tutor'
        comment_box = self.browser.find_element_by_id('id_comment')
        comment_box.send_keys('Frankin is very good Tutor.')

        # He click on submit button
        submit_button = self.browser.find_element_by_id('submit')
        submit_button.send_keys(Keys.ENTER)
        time.sleep(2)

        # After He submit his review
        # He could see his comment in review
        page_text = self.browser.find_element_by_id('review').text
        self.assertIn('Ronnie', page_text)
        self.assertIn('Frankin is very good Tutor.', page_text)

        # Then He logout from the website
        logout = self.browser.find_element_by_id('logout')
        logout.send_keys(Keys.ENTER)
        time.sleep(5)

        # Betty is also a student of Frankin
        # She have study with him for long time but he forget to review her tutor
        # Today, She decide to review her tutor Frankin

        # Betty login to spark website
        # ? self.login is login function for refactoring code
        self.login('betty', 'bettypassword')

        # Betty is going to review his tutor Frankin
        frankin = Tutor.objects.get(name='Frankin')
        self.browser.get(f'{self.live_server_url}/review/{frankin.id}')
        time.sleep(5)

        # She see Review in header of website
        header = self.browser.find_element_by_id('review-header').text
        self.assertEqual('Review', header)

        # And She see a review of Ronnie
        page_text = self.browser.find_element_by_id('review').text
        self.assertIn('Ronnie', page_text)
        self.assertIn('Frankin is very good Tutor.', page_text)

        # Betty see the comment box
        # So she type 'Frankin is the best tutor, I have ever seen in my life.'
        comment_box = self.browser.find_element_by_id('id_comment')
        comment_box.send_keys(
            'Frankin is the best tutor, I have ever seen in my life.')

        # She click on submit button
        submit_button = self.browser.find_element_by_id('submit')
        submit_button.send_keys(Keys.ENTER)
        time.sleep(5)

        # After She submit her review
        # She could see her comment in review
        page_text = self.browser.find_element_by_id('review').text
        self.assertIn('Betty', page_text)
        self.assertIn(
            'Frankin is the best tutor, I have ever seen in my life.', page_text)

        # Then She logout from the website
        logout = self.browser.find_element_by_id('logout')
        logout.send_keys(Keys.ENTER)
        time.sleep(5)

        # Frankin login to the website
        self.login('frankin', 'frankinpassword')

        # Frankin want to see the feedback from their student
        # So He go to review page to see reviews of him
        self.browser.get(f'{self.live_server_url}/review/{frankin.id}')
        time.sleep(5)

        # He see Review in header of website
        header = self.browser.find_element_by_id('review-header').text
        self.assertEqual('Review', header)

        # Frankin found that He is reviewed by his student Ronnie and Betty
        # He see their reviews
        page_text = self.browser.find_element_by_id('review').text
        self.assertIn('Ronnie', page_text)
        self.assertIn('Frankin is very good Tutor.', page_text)
        self.assertIn('Betty', page_text)
        self.assertIn(
            'Frankin is the best tutor, I have ever seen in my life.', page_text)
        time.sleep(5)

        self.fail('finish the test')

        #finish 
