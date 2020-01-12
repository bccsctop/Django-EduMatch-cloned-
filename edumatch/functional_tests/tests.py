from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time 
import unittest


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="/mnt/c/djangoProject/Django-EduMatch/geckodriver.exe")
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_for_one_user(self):

        #Mark is a student at some university. 
        #He feel very stressed about upcomming midterm exam.
        #His friend suggest a tutor-finder online app. So he goes
        # to check out its homepage.
         
        self.browser.get(self.live_server_url)

        #He notices the page title and header mention edumatch
        self.assertIn('edumatch',self.browser.title)

        #He could see a list of tutor user.
        #He select ploy to be his tutor.


        #He click on a ploy's match button.
        #The page will show that tutor ploy is match for him.
        self.fail('finist the test !!')
        

       
