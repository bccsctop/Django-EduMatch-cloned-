from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from selenium.webdriver.support.ui import Select
import time 
import unittest
from edu.models import Tutor 

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="/mnt/c/django/geckodriver.exe")
        #executable_path="/mnt/c/django/geckodriver.exe"
        frankin_user = User.objects.create_user('frankin','frankin@test.com','frankinpassword')
        ronnie_user = User.objects.create_user('ronnie','ronnie@test.com','ronniepassword')
        betty_user = User.objects.create_user('betty','betty@test.com','bettypassword')
        henderson_user = User.objects.create_user('henderson','henderson@test.com','hendersonpassword')
        frankin = Tutor.objects.create(user=frankin_user,name='Frankin',gender = 'Male',city = 'Bangkok',expert ='Statistic')
        ronnie = Tutor.objects.create(user=ronnie_user,name='Ronnie',gender = 'Male',city = 'Bangkok',expert ='Signal')
        betty = Tutor.objects.create(user=betty_user,name='Betty',gender = 'Female',city = 'Bangkok',expert ='Signal')
        henderson = Tutor.objects.create(user=henderson_user,name='Henderson',gender = 'Male',city = 'Chiangmai',expert ='Signal')


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
        self.assertIn('Betty',page_text)
        self.assertIn('Henderson',page_text)
        self.assertNotIn('Frankin',page_text)
        time.sleep(1)

        #Ronnie also logined , he notices that it has unique urls #Assume she login
        ronnie_id = Tutor.objects.get(name='Ronnie').id
        self.browser.get(f'{self.live_server_url}/lists/{ronnie_id}') 
        ronnie_url = self.browser.current_url
        self.assertRegex(ronnie_url,'/lists/.+')
        self.assertNotEqual(frankin_url,ronnie_url)

        #She found that he can match with frankin
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Frankin',page_text)
        self.assertIn('Betty',page_text)
        self.assertIn('Henderson',page_text)
        self.assertNotIn('Ronnie',page_text)
        time.sleep(1)

    def test_user_can_register_then_login_to_each_user_URL(self):

        #Mark is a student at KMUTNB(Bangkok). 
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

        #He see gender textbox. So he enter his gender
        #He types 'Male' into a text box
        gender_box = self.browser.find_element_by_id('id_gender')
        gender_box.send_keys('Male')

        #He see city textbox. So he enter his city
        #He types 'Bangkok' into a text box
        city_box = self.browser.find_element_by_id('id_city')
        city_box.send_keys('Bangkok')

        #He see subject textbox. So he enter his subject
        #He types 'Statistic' into a text box
        subject_box = self.browser.find_element_by_id('id_subject')
        subject_box.send_keys('Statistic')

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
        sign_in_button = self.browser.find_element_by_id('sign_in')
        sign_in_button.send_keys(Keys.ENTER)
        time.sleep(1)

        #He mention that he is already login 

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hi Mark_kmutnb!',page_text)

        #He found  a ton of user he can match with.
        self.assertIn('Ronnie',page_text)
        self.assertIn('Frankin',page_text)
        self.assertIn('Betty',page_text)
        self.assertIn('Henderson',page_text)

        #He want to study more about Signal Subject
        #Then he see textbox with "Enter your Subject that you need help!!!".
        #So he enter subject that he want to learn straight away.
        #He types "Signal" into a text box
        inputbox = self.browser.find_element_by_id('user_select_subject')  
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter your Subject that you need help!!!'
        )
        inputbox.send_keys('Signal')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(5)

        #After that he still see a ton of tutor user that agree 
        #to teach with that subject 
        table = self.browser.find_element_by_id('user_list_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertNotIn('Frankin', [row.text for row in rows])
        self.assertIn('Ronnie', [row.text for row in rows])
        self.assertIn('Betty', [row.text for row in rows])
        self.assertIn('Henderson', [row.text for row in rows])
        time.sleep(1)

        #So he realize that he dont't want to go far from his City
        #and he's a shy guy so he want to student with same gender
        #Then he see drop down with city and gender option
        #He select "Male" and "Bangkok" from dropdown
        inputbox = self.browser.find_element_by_id('user_select_subject') 
        gender_dropdown = Select(self.browser.find_element_by_id('user_select_gender'))  
        city_dropdown = Select(self.browser.find_element_by_id('user_city_subject'))  
        gender_dropdown.select_by_visible_text('Male')
        city_dropdown.select_by_visible_text('Bangkok')
        inputbox.send_keys('Signal')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(5)

        #After that he still see a ton of tutor user that agree 
        #to teach with that subject 
        table = self.browser.find_element_by_id('user_list_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertNotIn('Frankin', [row.text for row in rows])
        self.assertIn('Ronnie', [row.text for row in rows])
        self.assertNotIn('Betty', [row.text for row in rows])
        self.assertNotIn('Henderson', [row.text for row in rows])
        time.sleep(1)

        #He select Ronnie to be his tutor.
        #He click on a Ronnie's match button.
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

        sign_in_button = self.browser.find_element_by_id('sign_in')
        sign_in_button.send_keys(Keys.ENTER)
        time.sleep(1)

        #He mention that he is already login 

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hi frankin!',page_text)

        #He found that he can match with ronnie and new User named Mark
        self.assertIn('Ronnie',page_text)
        self.assertIn('Mark',page_text)

        self.fail('finist the test !!')
         

    
    def test_user_can_view_profile(self):

        #Frankin is a student at KMUTNB(Bangkok). 
        #His has member
        #He wants to see his profile
        # to check out its homepage.
        self.browser.get(self.live_server_url)

        #He notices the page title and header mention SPARK
        self.assertIn('SPARK',self.browser.title)

        #He found register and then he click it to register his ID

        register = self.browser.find_element_by_id('login')
        register.send_keys(Keys.ENTER)
        time.sleep(1)

        #He see form for Login
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('LOGIN',header_text)

        #He see textbox with "Username".So he enter username
        #He types "frankin" into a text box
        username_box = self.browser.find_element_by_id('id_username') 
        username_box.send_keys('frankin')
        

        #He see textbox with "Password".So he enter password
        #He types "frankinpassword" into a text box
        password1_box = self.browser.find_element_by_id('id_password')  
        password1_box.send_keys('frankinpassword')

        #He click on a Sign_in button.
        sign_in_button = self.browser.find_element_by_id('sign_in')
        sign_in_button.send_keys(Keys.ENTER)
        time.sleep(1)

        #He mention that he is already login 
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hi frankin!',page_text)

        #He wants to see his profile
        self.browser.get(self.live_server_url+"/profile")

        #He see form for Prrfile
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('PROFILE',header_text)

        #He see his username
        username = self.browser.find_element_by_tag_name('p1').text
        self.assertIn('frankin',username)  

        #He see his firstname
        firstname = self.browser.find_element_by_tag_name('p2').text
        self.assertIn('Firstname',firstname)  

        #He see his lastname
        lastname = self.browser.find_element_by_tag_name('p3').text
        self.assertIn('Lastname',lastname)

        #He see his gender
        gender = self.browser.find_element_by_tag_name('p4').text
        self.assertIn('Male',gender)

        #He see his city
        city = self.browser.find_element_by_tag_name('p5').text
        self.assertIn('Bangkok',city)

        #He see his expert
        expert = self.browser.find_element_by_tag_name('p6').text
        self.assertIn('Statistic',expert)


        self.fail('finist the test !!')

