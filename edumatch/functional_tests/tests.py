from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
import time 
import unittest
from edu.models import Tutor 

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="/mnt/c/django/geckodriver.exe")
        #executable_path="/mnt/c/django/geckodriver.exe"
        frankin_user = User.objects.create_user('frankin','frankin@test.com','frankinpassword')
        ronnie_user = User.objects.create_user('ronnie','ronnie@test.com','ronniepassword')
        frankin = Tutor.objects.create(user=frankin_user,name='Frankin',expert ='Statistic')
        ronnie = Tutor.objects.create(user=ronnie_user,name='Ronnie',expert ='Signal')

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

    def test_user_can_register_then_login_to_each_user_URL(self):

        #Mark is a student at some university. 
        #He feel very stressed about upcomming midterm exam.
        #His friend suggest a tutor-finder online app. So he goes
        # to check out its homepage.
        self.browser.get(self.live_server_url)

        #He notices the page title and header mention SPARK
        self.assertIn('SPARK',self.browser.title)

        #He found register and then he click it to register his ID

        register = self.browser.find_element_by_id('register')
        register.send_keys(Keys.ENTER)
        time.sleep(1)

        #He notices the page title and header mention register
        self.assertIn('REGISTER',self.browser.title)

        #He see register
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('REGISTER',header_text)

        #He see textbox with "Username".So he enter username
        #He types "Mark_kmutnb" into a text box
        username_box = self.browser.find_element_by_id('id_username') 
        username_box.send_keys('Mark_kmutnb')
        
        #He see textbox with "Password".So he enter password
        #He types "m9724617" into a text box
        password1_box = self.browser.find_element_by_id('id_password1')  
        password1_box.send_keys('m9724617')

        #He see textbox with "First name".So he enter first name
        #He types "Mark" into a text box
        name_box = self.browser.find_element_by_id('id_first_name')  
        name_box.send_keys('Mark')

        #He see textbox with "Last name".So he enter lastname
        #He types "Parker" into a text box
        lastname_box = self.browser.find_element_by_id('id_last_name')  
        lastname_box.send_keys('Parker')

        #He see textbox with "Password confirmation".So he enter password confirmation
        #He types "m9724617" into a text box
        password2_box = self.browser.find_element_by_id('id_password2')  
        password2_box.send_keys('m9724617')

        #He click on a Register button.
        sign_up_button = self.browser.find_element_by_name('sign_up')
        sign_up_button.send_keys(Keys.ENTER)
        time.sleep(1)
        
        #He see form for Login
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('LOGIN',header_text)

        #He see textbox with "Username".So he enter username
        #He types "Mark" into a text box
        username_box = self.browser.find_element_by_id('id_username') 
        username_box.send_keys('Mark_kmutnb')
        

        #He see textbox with "Password".So he enter password
        #He types "m9724617" into a text box
        password1_box = self.browser.find_element_by_id('id_password')  
        password1_box.send_keys('m9724617')

        #He click on a Register button.
        sign_in_button = self.browser.find_element_by_name('sign_in')
        sign_in_button.send_keys(Keys.ENTER)
        time.sleep(1)

        #He mention that he is already login 

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hi Mark_kmutnb!',page_text)

        #He found that he can match with ronnie and frankin
        self.assertIn('Ronnie',page_text)
        self.assertIn('Frankin',page_text)

        #He want to match with Ronnie So He click match on Ronnie

        button = self.browser.find_element_by_name('Ronnie')
        button.send_keys(Keys.ENTER)
        time.sleep(1)

        #The page will show that tutor Ronnie is match for him.
        result = self.browser.find_element_by_id('match_result')
        self.assertEqual(result.text,'match!!!')
        
        #Then He decide to log out from this web
        logout = self.browser.find_element_by_id('logout')
        logout.send_keys(Keys.ENTER)
        time.sleep(1)

        #The page will show that You are not logged in 
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('You are not logged in',page_text)


        #Frankin come back from work then he loggin to spark 
        
        
        login = self.browser.find_element_by_id('login')
        login.send_keys(Keys.ENTER)
        time.sleep(1)

        username_box = self.browser.find_element_by_id('id_username') 
        username_box.send_keys('frankin')
        
        password1_box = self.browser.find_element_by_id('id_password')  
        password1_box.send_keys('frankinpassword')

        sign_in_button = self.browser.find_element_by_name('sign_in')
        sign_in_button.send_keys(Keys.ENTER)
        time.sleep(1)

        #He mention that he is already login 

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hi frankin!',page_text)

        #He found that he can match with ronnie and new User named Mark
        self.assertIn('Ronnie',page_text)
        self.assertIn('Mark',page_text)

        self.fail('finist the test !!')
         
