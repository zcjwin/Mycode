import time

from selenium import webdriver
from PIL import Image
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Urbtix.process_captcha_image import *


def getCaptchaImage():
    # 设置无头浏览器
    opt = webdriver.ChromeOptions()
    # opt.set_headless()
    driver = webdriver.Chrome(options=opt)
    driver.maximize_window()
    driver.get('http://www.urbtix.hk/')
    WebDriverWait(driver,10,0.5).until(EC.visibility_of_element_located((By.LINK_TEXT,'登入')))
    driver.find_element_by_class_name('mem-login-state-link').click()
    WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.ID,'captchaImage')))
    time.sleep(2)
    # 获取验证码图片
    currentpage = './image/currentpage.png'
    driver.save_screenshot(currentpage)
    # 找到验证码元素的节点id
    captchaImage_element = driver.find_element_by_id('captchaImage')
    # print(captchaImage_element.location)  # 打印验证码元素的坐标位置
    # print(captchaImage_element.size)      # 打印验证码元素的大小
    left = captchaImage_element.location['x']
    top = captchaImage_element.location['y']
    right = captchaImage_element.location['x'] + captchaImage_element.size['width']
    bottom = captchaImage_element.location['y'] + captchaImage_element.size['height']
    # 找到验证码的位置并保存
    image = Image.open(currentpage)
    image = image.crop((left,top,right,bottom))
    image.save('./image/capimg.png')
    # 获取每一个点击验证码图片
    click_captchaImage1 = driver.find_elements_by_xpath('//form/div/div/table/tbody/tr/td/table/tbody/tr[@class="login-tbl-captcha-image-row captcha-row"][3]/td/table/tbody/tr/td/img')
    # print(len(click_captchaImage1)) # 打印点击验证码所有节点的长度
    for i,img in enumerate(click_captchaImage1):
        # print(img.location) # 每个点击验证码的坐标位置
        left =img.location['x']
        top =img.location['y']
        right =img.location['x'] + img.size['width']
        bottom =img.location['y'] + img.size['height']
        img = Image.open(currentpage)
        img =img.crop((left,top,right,bottom))
        img.save('./image/' + str(i) + '.png')

    # 整个点击验证码的图片
    tb_captchaImage = driver.find_element_by_xpath('//form/div/div/table/tbody/tr/td/table/tbody/tr[@class="login-tbl-captcha-image-row captcha-row"][3]/td/table')
    left = tb_captchaImage.location['x']
    top = tb_captchaImage.location['y']
    right = tb_captchaImage.location['x'] + tb_captchaImage.size['width']
    bottom = tb_captchaImage.location['y'] + tb_captchaImage.size['height']
    tb_captchaImage = Image.open(currentpage)
    tb_captchaImage = tb_captchaImage.crop((left,top,right,bottom))
    tb_captchaImage.save('./image/clicapimg/tbclicapimg.png')
    process_captcha_image()

if __name__ == '__main__':
    getCaptchaImage()












