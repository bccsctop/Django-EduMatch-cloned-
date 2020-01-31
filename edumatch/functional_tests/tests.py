from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time 
import unittest
from edu.models import Tutor 

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        #executable_path="/mnt/c/django/geckodriver.exe"
        frankin = Tutor.objects.create(name='Frankin',expert ='Statistic')
        ronnie = Tutor.objects.create(name='Ronnie',expert ='Signal')

    def tearDown(self):
        self.browser.quit()


    def wait_for_row_in_list_table(self,row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('user_list_table')
                rows = table.find_elements_by_tag_name('td')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_match_for_one_user(self):
        #Mark is a student at some university. 
        #He feel very stressed about upcomming midterm exam.
        #His friend suggest a tutor-finder online app. So he goes
        # to check out its homepage.
         
        self.browser.get(self.live_server_url)

        #He notices the page title and header mention SPARK
        self.assertIn('SPARK',self.browser.title)

        #He see a ton of Tutor list in that website 
        self.wait_for_row_in_list_table('Frankin')
        self.wait_for_row_in_list_table('Ronnie')
        time.sleep(1)
        #He see textbox with "Subject".So he enter subject that he
        #want to learn straight away.
        #He types "Signal" into a text box
        inputbox = self.browser.find_element_by_id('user_select_subject')  
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter your Subject that you need help!!!'
        )
        inputbox.send_keys('Signal')
        time.sleep(1)

        #After that he could see a list of tutor user that agree
        #to teach with that subject that he enter.
        table = self.browser.find_element_by_id('user_list_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn('Ronnie', [row.text for row in rows])
        time.sleep(1)
        #He select Ronnie to be his tutor.
        #He click on a Ronnie's match button.

        button = table.find_element_by_name('Ronnie')
        button.send_keys(Keys.ENTER)
    
        #The page will show that tutor Ronnie is match for him.
        result = self.browser.find_element_by_id('match_result')
        self.assertEqual(result.text,'match!!!')
        

    def test_multiple_users_can_login_to_different_urls(self):
        #Frankin logins to his spark web application 
        #(wait for login function to be completed so assume frankin was logined)
        #when he has logined , he notices that it has unique urls 
        frankin_id = Tutor.objects.get(name='Frankin').id
        self.browser.get(f'{self.live_server_url}/lists/{frankin_id}') 
        frankin_url = self.browser.current_url
        self.assertRegex(frankin_url,'/lists/.+')

        #He found that he can match with ronnie
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Ronnie',page_text)
        self.assertNotIn('Frankin',page_text)
        time.sleep(1)

        #Ronnie also logined , he notices that it has unique urls #Assume he login
        ronnie_id = Tutor.objects.get(name='Ronnie').id
        self.browser.get(f'{self.live_server_url}/lists/{ronnie_id}') 
        ronnie_url = self.browser.current_url
        self.assertRegex(ronnie_url,'/lists/.+')
        self.assertNotEqual(frankin_url,ronnie_url)

        #He found that he can match with frankin
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Frankin',page_text)
        self.assertNotIn('Ronnie',page_text)
        time.sleep(1)


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        #executable_path="/mnt/c/django/geckodriver.exe"

    def tearDown(self):
        self.browser.quit()


    def test_can_register_user(self):
        #Mark Parker is a student at some university. 
        #He has no members.
        #So he goes to register.
        self.browser.get('http://127.0.0.1:8000/register')

        #He notices the page title and header mention register
        self.assertIn('REGISTER',self.browser.title)
        

        #He see form for register
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('REGISTER',header_text)

        

        #He see textbox with "Username".So he enter username
        #He types "Mark" into a text box
        username_box = self.browser.find_element_by_id('id_username') 
        username_box.send_keys('Mark')
        

        #He see textbox with "Password".So he enter password
        #He types "m123456" into a text box
        password1_box = self.browser.find_element_by_id('id_password1')  
        password1_box.send_keys('m12345678')

        #He see textbox with "First name".So he enter first name
        #He types "Mark" into a text box
        name_box = self.browser.find_element_by_id('id_first_name')  
        name_box.send_keys('Mark')

        #He see textbox with "Last name".So he enter lastname
        #He types "Parker" into a text box
        lastname_box = self.browser.find_element_by_id('id_last_name')  
        lastname_box.send_keys('Parker')

        #He see textbox with "Password confirmation".So he enter password confirmation
        #He types "m123456" into a text box
        password2_box = self.browser.find_element_by_id('id_password2')  
        password2_box.send_keys('m12345678')



        #He click on a Register button.
        sign_up_button = self.browser.find_element_by_name('sign_up')
        sign_up_button.send_keys(Keys.ENTER)
        time.sleep(1)
        

        self.fail('finist the test !!')

    def test_can_login_user(self):
        #Mark Parker is a student at some university. 
        #He has members.
        #So he goes to login.
        self.browser.get('http://127.0.0.1:8000/accounts/login/')

        #He see form for Login
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('LOGIN',header_text)

        #He see textbox with "Username".So he enter username
        #He types "Mark" into a text box
        username_box = self.browser.find_element_by_id('id_username') 
        username_box.send_keys('Mark')
        

        #He see textbox with "Password".So he enter password
        #He types "m123456" into a text box
        password1_box = self.browser.find_element_by_id('id_password')  
        password1_box.send_keys('m12345678')

        #He click on a Register button.
        sign_in_button = self.browser.find_element_by_name('sign_in')
        sign_in_button.send_keys(Keys.ENTER)
        time.sleep(1)


        self.fail('finist the test !!')

        
        



       
