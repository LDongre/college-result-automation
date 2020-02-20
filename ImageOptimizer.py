from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
import urllib.request
from pytesseract import image_to_string
import numpy as np
import cv2

Img_blur = 6
Img_thresh = 127
Img_kernal = 4

for img_blur in range(0, Img_blur):
    for img_kernal in range(4):
        image = cv2.imread('Captcha Images/captcha.png', 0)
        # cv2.imshow('image', image)

        image = cv2.blur(image, (3, 3))
        # cv2.imshow('blur', image)

        _, image = cv2.threshold(image, Img_thresh, 255, cv2.THRESH_BINARY)
        # cv2.imshow('thresh', image)

        kernal = np.ones((img_kernal, img_kernal), np.uint8)
        image = cv2.dilate(image, kernal, iterations=2)
        # cv2.imshow('dilate', image)

        cv2.imwrite('CaptchaExp/img blur=' + str(img_blur) + "thresh=" + str(Img_thresh) + 'kernal=' + str(img_kernal) + '.png', image)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

# th3 = cv2.adaptiveThreshold(thresh,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,8)
# cv2.imshow('th3', th3)

# print(image.shape)

# cv2.imwrite('Captcha Images/decoded.png', thresh)
# captcha_text = image_to_string(thresh, config="-c tessedit_char_whitelist=ACDEFGHJKLMNPQRTUVWXYZ2346789")

# print(captcha_text)
