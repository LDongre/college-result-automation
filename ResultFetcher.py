import time
import cv2
import urllib.request
from pytesseract import image_to_string
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select

import ImageOptimizer2 as io2


class Student:
    name = ''
    rollno = ''
    branch = ''
    course = ''
    sem = ''
    sgpa = ''

    def display(self):
        print('name:', self.name)
        print('rollno:', self.rollno)
        print('branch:', self.branch)
        print('course:', self.course)
        print('sem:', self.sem)
        print('sgpa:', self.sgpa)


# Key variables
COURSE = 'BTech'
CLG_CODE = '0101'
BRANCH = 'CS'
ROLL_START = 171015
ROLL_END = 171069
SEM = '5'

# launch instance of firefox
binary = FirefoxBinary('/etc/firefox/firefox')
driver = webdriver.Firefox(firefox_binary=binary)
driver.get('http://www.uitrgpv.ac.in/Exam/ProgramSelect.aspx')

# select course
btech_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[4]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td[5]/label'
btech = driver.find_element_by_xpath(btech_xpath)
btech.click()

for number in range(ROLL_START, ROLL_START + 10):


    captcha_decoded = False

    while not captcha_decoded:

        try:
            studentNo = CLG_CODE + BRANCH + str(number)

            rollno_xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtrollno"]'
            rollno = driver.find_element_by_xpath(rollno_xpath)
            rollno.send_keys(studentNo)

            sem_xpath = '//*[@id="ctl00_ContentPlaceHolder1_drpSemester"]'
            sem = Select(driver.find_element_by_xpath(sem_xpath))
            sem.select_by_visible_text(SEM)

            # download captcha image
            captcha_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[4]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/div/img'
            captcha = driver.find_element_by_xpath(captcha_xpath)

            captcha_src = captcha.get_attribute('src')
            urllib.request.urlretrieve(captcha_src, 'Captcha Images/captcha' + studentNo + '.png')

            # load image
            image = cv2.imread('Captcha Images/captcha' + studentNo + '.png', 0)

            # remove noise
            image = io2.erode(io2.thold(io2.med_blur(image, 5), 127), 2, 2)

            # read image
            captcha_text = image_to_string(image, config="-c tessedit_char_whitelist=ACDEFGHJKLMNPQRTUVWXYZ2346789")

            captcha_text = captcha_text if captcha_text is not None else 'EMPTY'
            print(captcha_text)

            time.sleep(2)

            # fill captcha
            captcha_field_xpath = '//*[@id="ctl00_ContentPlaceHolder1_TextBox1"]'
            captcha_field = driver.find_element_by_xpath(captcha_field_xpath)
            captcha_field.clear()
            captcha_field.send_keys(captcha_text)

            if captcha_text == '':
                print("EMPTY CAPTCHA")

            # click submit button
            submit_xpath = '//*[@id="ctl00_ContentPlaceHolder1_btnviewresult"]'
            submit = driver.find_element_by_xpath(submit_xpath)
            submit.click()

        except:
            time.sleep(2)
            # reset form
            reset_xpath = '//*[@id="ctl00_ContentPlaceHolder1_btnReset"]'
            reset = driver.find_element_by_xpath(reset_xpath)
            reset.click()
            captcha_decoded = True

        try:
            student = Student()

            # finding student details
            st_name_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblNameGrading"]'
            st_name = driver.find_element_by_xpath(st_name_xpath)
            student.name = st_name.text if st_name.text is not None else ''

            st_rollno_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblRollNoGrading"]'
            st_rollno = driver.find_element_by_xpath(st_rollno_xpath)
            student.rollno = st_rollno.text if st_rollno.text is not None else ''

            st_branch_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblBranchGrading"]'
            st_branch = driver.find_element_by_xpath(st_branch_xpath)
            student.branch = st_branch.text if st_branch.text is not None else ''

            student.course = COURSE
            student.sem = SEM

            st_sgpa_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblSGPA"]'
            st_sgpa = driver.find_element_by_xpath(st_sgpa_xpath)
            student.sgpa = st_sgpa.text if st_sgpa.text is not None else ''

            student.display()

            captcha_decoded = True

            # reset form
            reset_xpath = '//*[@id="ctl00_ContentPlaceHolder1_btnReset"]'
            reset = driver.find_element_by_xpath(reset_xpath)
            reset.click()

        except:
            pass
