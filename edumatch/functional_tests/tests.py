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
        self.browser = webdriver.Firefox()
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
        gender_box = Select(self.browser.find_element_by_id('id_gender'))
        gender_box.select_by_visible_text('Male')


        #He see city textbox. So he enter his city
        #He types 'Bangkok' into a text box
        city_box = Select(self.browser.find_element_by_id('id_city'))
        city_box.select_by_visible_text('Bangkok')

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
        time.sleep(2)

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
        time.sleep(2)

        #After that he could see a tutor user that agree 
        #to teach with that subject with his condition
        table = self.browser.find_element_by_id('user_list_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertNotIn('Frankin', [row.text for row in rows])
        self.assertIn('Ronnie', [row.text for row in rows])
        self.assertNotIn('Betty', [row.text for row in rows])
        self.assertNotIn('Henderson', [row.text for row in rows])
        time.sleep(1)

        #He select Ronnie to be his tutor.
        #He click on a Ronnie's match button.
        ronnie_id = Tutor.objects.get(name='Ronnie').id
        button = self.browser.find_element_by_xpath(f"//a[contains(@href,'match-request/send/{ronnie_id}')]")
        button.send_keys(Keys.ENTER)
        time.sleep(2)
        #The page will refresh and Ronnie's match button change to Ronnie's cancel-match button
        #because his request has been sent and he can cancel his request by this cancel-match button.
        table = self.browser.find_element_by_id('user_list_table')
        rows = table.find_elements_by_tag_name('td')
        cancelButton = self.browser.find_elements_by_tag_name('a')
        self.assertIn('Frankin', [row.text for row in rows])
        self.assertIn('Ronnie', [row.text for row in rows])
        self.assertIn('Betty', [row.text for row in rows])
        self.assertIn('Henderson', [row.text for row in rows])
        self.assertIn('Cancel',[ i.text for i in cancelButton])
        time.sleep(2)

        #He wants to see his request so he goes to match-result page
        self.browser.get(self.live_server_url+"/match-result")
        time.sleep(2)

        #He see three topic in match-result page.
        requestHeader_texts = self.browser.find_elements_by_tag_name('h1')
        self.assertIn('My Tutor/Student',[ i.text for i in requestHeader_texts])
        self.assertIn('Sent Tutor Requests',[i.text for i in requestHeader_texts])
        self.assertIn('Received Tutor Requests',[i.text for i in requestHeader_texts])

        #He see that in Sent Match Requests topic has ronnie's name
        #the person who has recieve match request that him sent
        requestSent_text = self.browser.find_element_by_id('sent_request_item').text
        self.assertIn('ronnie',requestSent_text)
        
        #Then He decide to log out from this web
        logout = self.browser.find_element_by_id('logout')
        logout.send_keys(Keys.ENTER)
        time.sleep(1)

        #The page will show that You are not logged in 
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('You are not logged in',page_text)

        #Ronnie come back from work then he loggin to spark 
        login = self.browser.find_element_by_id('login')
        login.send_keys(Keys.ENTER)
        time.sleep(1)

        #He see textbox with "Username".So he enter username
        #He types "ronnie" into a text box
        username_box = self.browser.find_element_by_id('id_username') 
        username_box.send_keys('ronnie')
        
        #He see textbox with "Password".So he enter password
        #He types "ronniepassword" into a text box
        password1_box = self.browser.find_element_by_id('id_password')  
        password1_box.send_keys('ronniepassword')

        #He click on a sign_in button.
        sign_in_button = self.browser.find_element_by_id('sign_in')
        sign_in_button.send_keys(Keys.ENTER)
        time.sleep(1)

        #He mention that he is already login 
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hi ronnie!',page_text)

        #He found that he can match with Frankin,Betty,Henderson and new User named Mark
        self.assertIn('Frankin',page_text)
        self.assertIn('Mark',page_text)
        self.assertIn('Betty',page_text)
        self.assertIn('Henderson',page_text)

        #He want to see if anyone has sent a match-request to him
        #So he go to match-result page
        self.browser.get(self.live_server_url+"/match-result")
        time.sleep(1)

        #He see three topic in match-result page.
        requestHeader_texts = self.browser.find_elements_by_tag_name('h1')
        self.assertIn('My Tutor/Student',[ i.text for i in requestHeader_texts])
        self.assertIn('Sent Tutor Requests',[i.text for i in requestHeader_texts])
        self.assertIn('Received Tutor Requests',[i.text for i in requestHeader_texts])

        #In Received Match Requests part,He see that Mark_kmutnb has sent match request
        #to him and he notice two button is Accept and Reject button
        requestHeader_texts = self.browser.find_elements_by_tag_name('a')
        self.assertIn('Mark_kmutnb',[ i.text for i in requestHeader_texts])
        self.assertIn('Accept',[i.text for i in requestHeader_texts])
        self.assertIn('Reject',[i.text for i in requestHeader_texts])

        #He agrees to be mark tutor so he click at Accept button 
        mark_id = Tutor.objects.get(name='Mark').id
        button = self.browser.find_element_by_xpath(f"//a[contains(@href,'/match-request/accept/{mark_id}')]")
        button.send_keys(Keys.ENTER)
        time.sleep(2)

        #After that Mark has change position in to Contact part
        requestHeader_texts = self.browser.find_elements_by_tag_name('a')
        self.assertIn('Mark_kmutnb(Offline)',[ i.text for i in requestHeader_texts])

        #Then He decide to log out from this web
        logout = self.browser.find_element_by_id('logout')
        logout.send_keys(Keys.ENTER)
        time.sleep(1)

        #The page will show that You are not logged in 
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('You are not logged in',page_text)

        #The next day Mark came back from his class then he loggin to spark 
        login = self.browser.find_element_by_id('login')
        login.send_keys(Keys.ENTER)
        time.sleep(1)

        #He see textbox with "Username".So he enter username
        #He types "Mark_kmutnb" into a text box
        username_box = self.browser.find_element_by_id('id_username') 
        username_box.send_keys('Mark_kmutnb')
        
        #He see textbox with "Password".So he enter password
        #He types "m9724617" into a text box
        password1_box = self.browser.find_element_by_id('id_password')  
        password1_box.send_keys('m9724617')

        #He click on a sign_in button.
        sign_in_button = self.browser.find_element_by_id('sign_in')
        sign_in_button.send_keys(Keys.ENTER)
        time.sleep(1)

        #He mention that he is already login 
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hi Mark_kmutnb!',page_text)

        #He want to know that ronnie has accept his request yet or not
        #So he want to match-result page to check it.
        self.browser.get(self.live_server_url+"/match-result")
        time.sleep(1)

        #He see ronnie at Contact part so he decide to chat with hime later...
        requestHeader_texts = self.browser.find_elements_by_tag_name('a')
        self.assertIn('ronnie(Offline)',[ i.text for i in requestHeader_texts])

        self.fail('finist the test !!')
         

    
    def test_user_can_view_profile_and_edit_profile(self):

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

        #He click on a Profile button.
        profile_button = self.browser.find_element_by_id('profile_btn')
        profile_button.send_keys(Keys.ENTER)
        time.sleep(1)

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

        #But he see that Profile was wrong, so he solved it.
        profile_button = self.browser.find_element_by_id('edit')
        profile_button.send_keys(Keys.ENTER)
        time.sleep(1)

        #He see city textbox. So he therefore resolved from Bangkok to Nonthaburi.
        #He types 'Nonthaburi' into a text box
        city_box = Select(self.browser.find_element_by_id('id_city'))
        city_box.select_by_visible_text('Nonthaburi')

        #He click on a Confirm button.
        edit_confirm_button = self.browser.find_element_by_id('edit_confirm')
        edit_confirm_button.send_keys(Keys.ENTER)
        time.sleep(1)

        #He see form for Prrfile
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('PROFILE',header_text)

        #He see his city
        city = self.browser.find_element_by_tag_name('p5').text
        self.assertNotIn('Bangkok',city)
        self.assertIn('Nonthaburi',city)

        #After he finished watching, he returned to the home page.
        home_button = self.browser.find_element_by_id('home')
        home_button.send_keys(Keys.ENTER)
        time.sleep(1)

        #He notices the page title and header mention SPARK
        self.assertIn('SPARK',self.browser.title)



        self.fail('finist the test !!')

