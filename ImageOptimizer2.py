from pytesseract import image_to_string
import os
import numpy as np
import cv2

# BLUR = [1, 3, 5]  # must be odd
# THRESH = 127
# E_KER = [0, 1, 2, 3, 4]
# D_KER = [0]
# D_IT = [0]
# E_IT = [0, 1, 2, 3]
# OEM = [1]
# PSM = [8]
WHITELIST = 'ACDEFGHJKLMNPQRTUVWXYZ2346789'
# CAPTCHA_DIR = 'Captcha Images'


def img2txt(img, psm_val, oem_val):
    tess_str = "-c tessedit_char_whitelist={} --psm {} --oem {}"
    captcha_text = image_to_string(img, config=tess_str.format(WHITELIST, psm_val, oem_val))
    return captcha_text


def img2txt_pnt(img, psm_val, oem_val):
    print(img2txt(img, psm_val, oem_val))


def show_img(img, name):
    cv2.imshow(img, name)


def med_blur(img, amt):
    return cv2.medianBlur(img, amt)


def thold(img, amt):
    _, thresh = cv2.threshold(img, amt, 255, cv2.THRESH_BINARY)
    return thresh


def dilate(img, k_size, it):
    ker = np.ones((k_size, k_size), np.uint8)
    return cv2.dilate(img, ker, it)


def erode(img, k_size, it):
    ker = np.ones((k_size, k_size), np.uint8)
    return cv2.erode(img, ker, it)


# files = os.listdir(CAPTCHA_DIR)
#
# for i in range(0, len(files)):
#     print('************************************************')
#     print('FILENAME', files[i])
#     for blur in BLUR:
#         for e_ker in E_KER:
#             # for d_ker in D_KER:
#             for e_it in E_IT:
#                 # for d_it in D_IT:
#                 for oem in OEM:
#                     image = cv2.imread(os.path.join(CAPTCHA_DIR, files[i]), 0)
#                     image = erode(thold(med_blur(image, blur), THRESH), e_ker, e_it)
#                     res = img2txt(image, PSM[0], oem)
#                     # result = 'psm={},oem={},blur={},e_ker={},e_it={}'
#                     # print(res, result.format(PSM[0], oem, blur, e_ker, e_it))
#                     if os.path.splitext(files[i])[0].upper() == res:
#                         result = 'JACKPOT: blur={},e_ker={},e_it={}'
#                         print(result.format(blur, e_ker, e_it))

# cv2.waitKey(0)
# cv2.destroyAllWindows()
