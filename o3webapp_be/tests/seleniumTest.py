import unittest
from time import sleep
from selenium import webdriver

class MyTestCase(unittest.TestCase):
    #Open the homepage, click "strat" to jump to the page,
    # click "submit" to generate a plot, and then save it as a PDF.
    def test(self):
        (self).driver = webdriver.Chrome()
        (self).driver.get('http://o3web.test.fedcloud.eu/')
        sleep(1)
        but = self.driver.find_element_by_class_name("startButton.mat-style-accent")
        but.click()
        subBut = self.driver.find_element_by_class_name("submit-button.mat-style-accent")
        subBut.click()
        pDFBUt = self.driver.find_element_by_class_name("mat-style-accent.download-button")
        pDFBUt.click()
        print(type(but))
        sleep(10)

    def test2(self):
        # Open the homepage, click "strat" to jump to the page,
        # click "submit" to generate a plot, add a group for mean,add a group for median,add a group for trend
        # and then save it as a PDF.
        (self).driver = webdriver.Chrome()
        (self).driver.get('http://o3web.test.fedcloud.eu/')
        sleep(1)
        subBut = self.driver.find_element_by_class_name("submit-button.mat-style-accent")
        subBut.click()
        meanBut = self.driver.find_element_by_link_text('mean')
        meanBut.click()
        medianBut = self.driver.find_element_by_link_text('median')
        medianBut.click()
        trendBut = self.driver.find_element_by_link_text('trend')
        trendBut.click()
        pDFBUt = self.driver.find_element_by_class_name("mat-style-accent.download-button")
        pDFBUt.click()
        sleep(10)
        # Open the homepage, click "strat" to jump to the page,
        # log in
        # click "submit" to generate a plot.
        # and then save it as a PDF.
    def test3(self):
        (self).driver = webdriver.Chrome()
        (self).driver.get('http://o3web.test.fedcloud.eu/')
        sleep(1)
        subBut = self.driver.find_element_by_class_name("submit-button.mat-style-accent")
        subBut.click()
        logBut = self.driver.find_element_by_id("login")
        logBut.click()
        account = self.driver.find_element_by_id("favouritesubmit")
        account.click()
        email = self.driver.find_element_by_id("identifierId")
        email.send_keys("denize0bao@gmail.com")
        pngBut = self.driver.find_element_by_link_text("PNG")
        csvBut = self.driver.find_element_by_link_text("CSV")
        pdfBut = self.driver.find_element_by_link_text("PDF")
        pngBut.click()
        csvBut.click()
        pdfBut.click()
        print(type(subBut))
        sleep(10)
    def test4(self):
        # Open the homepage, click "strat" to jump to the page,
        # log in
        # click "submit" to generate a plot, add a group for mean,add a group for median,add a group for trend
        # and then save it as a PDF.
        (self).driver = webdriver.Chrome()
        (self).driver.get('http://o3web.test.fedcloud.eu/')
        sleep(1)
        but = self.driver.find_element_by_class_name("startButton.mat-style-accent")
        but.click()
        subBut = self.driver.find_element_by_class_name("submit-button.mat-style-accent")
        subBut.click()
        logBut = self.driver.find_element_by_id("login")
        logBut.click()
        account = self.driver.find_element_by_id("favouritesubmit")
        account.click()
        email = self.driver.find_element_by_id("identifierId")
        email.send_keys("denize0bao@gmail.com")
        meanBut = self.driver.find_element_by_link_text('mean')
        meanBut.click()
        medianBut = self.driver.find_element_by_link_text('median')
        medianBut.click()
        trendBut = self.driver.find_element_by_link_text('trend')
        trendBut.click()
        pdfBut = self.driver.find_element_by_class_name("mat-style-accent.download-button")
        pdfBut.click()
        sleep(10)

    # Open the homepage, click "strat" to jump to the page,
    # log in.
    # click "submit" to generate a plot, add a group for mean,add a group for median,add a group for trend.
    # Remove components：mean, median and trend.
    # and then save it as a PDF.
    def test5(self):
        (self).driver = webdriver.Chrome()
        (self).driver.get('http://o3web.test.fedcloud.eu/')
        sleep(1)
        but = self.driver.find_element_by_class_name("startButton.mat-style-accent")
        but.click()
        subBut = self.driver.find_element_by_class_name("submit-button.mat-style-accent")
        subBut.click()
        logBut = self.driver.find_element_by_id("login")
        logBut.click()
        account = self.driver.find_element_by_id("favouritesubmit")
        account.click()
        email = self.driver.find_element_by_id("identifierId")
        email.send_keys("denize0bao@gmail.com")
        meanBut = self.driver.find_element_by_link_text('mean')
        meanBut.click()
        medianBut = self.driver.find_element_by_link_text('median')
        medianBut.click()
        trendBut = self.driver.find_element_by_link_text('trend')
        trendBut.click()
        reMeanBut = self.driver.find_element_by_link_text('meanremove')
        reMedianBut = self.driver.find_element_by_link_text('medianremove')
        reTrendBut = self.driver.find_element_by_link_text('trendremove')
        reMeanBut.click()
        reMedianBut.click()
        reTrendBut.click()
        pDFBUt = self.driver.find_element_by_class_name("mat-style-accent.download-button")
        pDFBUt.click()
        print(type(but))
        sleep(10)


        

if __name__ == '__main__':
    unittest.main()
