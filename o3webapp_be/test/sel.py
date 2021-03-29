import unittest
from time import sleep
from selenium import webdriver

class MyTestCase(unittest.TestCase):
    #Open the homepage, click "strat" to jump to the page,
    # click "submit" to generate a picture, and then save it as a PDF.
    def test(self):
        (self).driver = webdriver.Chrome()
        (self).driver.get('http://o3web.test.fedcloud.eu/')
        sleep(1)
        #self.driver.find_element_by_name('q').send_keys('KIT')
        but = self.driver.find_element_by_class_name("startButton.mat-style-accent")
        but.click()
        subBut = self.driver.find_element_by_class_name("submit-button.mat-style-accent")
        subBut.click()
        #meanBut = self.driver.find_element_by_link_text('mean')
        #meanBut.click
        pDFBUt = self.driver.find_element_by_class_name("mat-style-accent.download-button")
        pDFBUt.click()
        print(type(but))
        sleep(10)
   # def test2(self):

        

if __name__ == '__main__':
    unittest.main()
