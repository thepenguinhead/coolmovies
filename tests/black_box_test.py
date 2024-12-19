import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ReviewTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome()  # Web driver swapped for Chrome
        self.browser.get('http://127.0.0.1:5000/signup')
        self.browser.maximize_window()
        
    def tearDown(self):
        self.browser.quit()


    def test_new_review(self):  # Movie ID: tt13623148
        
        #loggin into admin account
        
        self.browser.get('http://127.0.0.1:5000/login')
        
        userName = self.browser.find_element(By.ID, 'username')
        userName.send_keys('admin')

        password = self.browser.find_element(By.ID, 'password')
        password.send_keys('password')

        submitButton = self.browser.find_elements(By.TAG_NAME, 'button')[2]
        submitButton.click()

        h2 = self.browser.find_elements(By.TAG_NAME, 'h2')[0].text
        self.assertEqual("Recommended Movies", h2)
        
        
        #------------------------------------------------------------------------------

        #create / delete review
        
        self.browser.get('http://127.0.0.1:5000/media/movie/tt14888874')
        
        reviewButton = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, "review_button")))
        reviewButton.click()

        starElement = WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable((By.ID, 'star5')))
        starElement.click()

        newComment = self.browser.find_element(By.ID, 'comment')
        newComment.send_keys('test')

        submitButton = self.browser.find_element(By.ID, 'submit_review')
        submitButton.click()

        page = self.browser.current_url
        self.assertEqual('http://127.0.0.1:5000/media/movie/tt14888874', page)

        reviewUsername = WebDriverWait(self.browser, 15).until(EC.visibility_of_element_located((By.ID, 'user_comment')))
        self.assertEqual('test', reviewUsername.text)

        deleteButton = self.browser.find_elements(By.TAG_NAME, 'button')[5]
        deleteButton.send_keys('\ue007')

        confirmDeleteButton = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, "confirm_delete")))
        confirmDeleteButton.click()
        
        confirmationMessage = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'no_reviews')))
        self.assertEqual(confirmationMessage.text, "Be The First To Review This Movie!")


if __name__ == '__main__':
    unittest.main()
