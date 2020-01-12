from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time 
import unittest
from edu.models import Tutor 

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="/mnt/c/djangoProject/Django-EduMatch/geckodriver.exe")
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_for_one_user(self):
        
        #set up database 
        first_tutor = Tutor()
        first_tutor.name = 'Mark'
        first_tutor.save()

        second_tutor = Tutor()
        second_tutor.name = 'Ploy'
        second_tutor.save()

        #Mark is a student at some university. 
        #He feel very stressed about upcomming midterm exam.
        #His friend suggest a tutor-finder online app. So he goes
        # to check out its homepage.
         
        self.browser.get(self.live_server_url)

        #He notices the page title and header mention edumatch
        self.assertIn('edumatch',self.browser.title)

        #He could see a list of tutor user.
        table = self.browser.find_element_by_id('user_list_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertTrue(
            any(row.text == 'Tutor: Ploy' for row in rows),
           f"Tutor: Ploy did not appear in table. Content were: \n{table.text}"
        )
        time.sleep(1)
        #He select ploy to be his tutor.
        #He click on a ploy's match button.

        button = table.find_element_by_name('Ploy')
        button.send_keys(Keys.ENTER)
    
        #The page will show that tutor ploy is match for him.
        result = self.browser.find_element_by_id('match_result')
        self.assertEqual(result.text,'match!!!')
        
        self.fail('finist the test !!')
        

       
