from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
import urllib.request
from pytesseract import image_to_string
import cv2


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

#Key variables
COURSE = 'BTech'
CLG_CODE = '0101'
BRANCH = 'CS'
ROLL_START = 171012
ROLL_END = 171069
SEM = '5'

#launch instance of firefox
binary = FirefoxBinary('/etc/firefox/firefox')
driver = webdriver.Firefox(firefox_binary=binary)
driver.get('http://www.uitrgpv.ac.in/Exam/ProgramSelect.aspx')

#select course
btech_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[4]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td[5]/label'
btech = driver.find_element_by_xpath(btech_xpath)
btech.click()

for number in range(ROLL_START, ROLL_START + 2):

    studentNo = CLG_CODE + BRANCH + str(number)

    rollno_xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtrollno"]'
    rollno = driver.find_element_by_xpath(rollno_xpath)
    rollno.send_keys(studentNo)

    sem_xpath = '//*[@id="ctl00_ContentPlaceHolder1_drpSemester"]'
    sem = Select(driver.find_element_by_xpath(sem_xpath))
    sem.select_by_visible_text(SEM)

    captcha_decoded = False

    while (captcha_decoded == False):

        #download captcha image
        captcha_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[4]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/div/img'
        captcha = driver.find_element_by_xpath(captcha_xpath)
        captcha_src = captcha.get_attribute('src')
        urllib.request.urlretrieve(captcha_src, 'Captcha Images/captcha' + studentNo + '.png')

        #remove noise
        image = cv2.imread('Captcha Images/captcha' + studentNo + '.png', 0)
        # cv2.imshow('image', image)

        blur = cv2.blur(image,(4,4))
        # cv2.imshow('blur', blur)

        ret,thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)

        # cv2.imshow('thresh', thresh)

        # th3 = cv2.adaptiveThreshold(thresh,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,8)
        # cv2.imshow('th3', th3)

        # print(image.shape)

        # cv2.imwrite('Captcha Images/decoded.png', thresh)
        captcha_text = image_to_string(thresh, config="-c tessedit_char_whitelist=ACDEFGHJKLMNPQRTUVWXYZ2346789")

        print(captcha_text)
        print(len(captcha_text))
        # test_xpath = '//*[@id="ctl00_ContentPlaceHolder1_"]'
        # test = driver.find_element_by_xpath(test_xpath)
        # if test is None:
        #     print('test is None')


        # fill captcha
        captcha_field_xpath = '//*[@id="ctl00_ContentPlaceHolder1_TextBox1"]'
        captcha_field = driver.find_element_by_xpath(captcha_field_xpath)
        captcha_field.clear()
        captcha_field.send_keys(captcha_text)

        if captcha_text == '':
            print("EMPTY CAPTCHA")

        #click submit button
        submit_xpath = '//*[@id="ctl00_ContentPlaceHolder1_btnviewresult"]'
        submit = driver.find_element_by_xpath(submit_xpath)
        submit.click()

        try:
            student = Student()

            # finding student details
            st_name_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblNameGrading"]'
            st_name = driver.find_element_by_xpath(st_name_xpath)
            student.name = st_name.text

            st_rollno_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblRollNoGrading"]'
            st_rollno = driver.find_element_by_xpath(st_rollno_xpath)
            student.rollno = st_rollno.text

            st_branch_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblBranchGrading"]'
            st_branch = driver.find_element_by_xpath(st_branch_xpath)
            student.branch = st_branch.text

            student.course = COURSE
            student.sem = SEM

            st_sgpa_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblSGPA"]'
            st_sgpa = driver.find_element_by_xpath(st_sgpa_xpath)
            student.sgpa = st_sgpa.text

            # print(student.name, student.rollno, student.branch, student.course, student.sem, student.sgpa)
            student.display()
            captcha_decoded = True

            #reset form
            reset_xpath='//*[@id="ctl00_ContentPlaceHolder1_btnReset"]'
            reset = driver.find_element_by_xpath(reset_xpath)
            reset.click()

        except:
            pass

