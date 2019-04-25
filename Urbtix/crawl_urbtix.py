import random
import time
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
from io import BytesIO
from Urbtix.random_userinfo import *


class CrawlUrbtix(object):
    def __init__(self):
        self.opt = webdriver.ChromeOptions()
        # self.opt.set_headless()
        # 创建浏览器对象
        self.driver = webdriver.Chrome(options=self.opt)
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        # self.url = 'http://msg.urbtix.hk/'
        self.url = 'http://www.urbtix.hk'

    def login(self):
        regis = self.register()
        info = random.choice(regis)
        # 点击登入到登录界面
        self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"登入")))
        self.driver.find_element_by_link_text('登入').click()
        # 填写登录信息
        self.driver.find_element_by_id('j_username').send_keys('zx18612015735')
        self.driver.find_element_by_id('j_password').send_keys('123456')
        # 验证码
        time.sleep(5)

        # 点击登入按钮
        self.driver.find_element_by_class_name('btn-inner-blk').click()

    # 注册信息界面
    def register(self):
        info_list = []
        with codecs.open('infomation.txt','w','utf-8') as f:
            infocount = int(input("请输入您要随机生成的注册信息数量："))
            for count in range(infocount):
                info_dict = {}
                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"登入")))
                self.driver.find_element_by_link_text('登入').click()
                # 等待继续按钮元素加载完再执行点击
                try:
                    self.wait.until(EC.visibility_of_element_located(
                        (By.XPATH,'//table/tbody/tr/td/div/div/div[@class="member-login-become-member"]/div/div/span')))
                except TimeoutException as e:
                    print(e)
                # 点击继续到注册页面
                self.driver.find_element_by_xpath('//table/tbody/tr/td/div/div/div[@class="member-login-become-member"]/div/div/span').click()
                surname = getSurname()
                self.driver.find_element_by_id('surname').send_keys(surname)
                info_dict['surname'] = surname
                firstName = getfirstName()
                self.driver.find_element_by_id('firstName').send_keys(firstName)
                info_dict['firstName'] = firstName
                contactPhoneNo = getTelNo()
                self.driver.find_element_by_id('contactPhoneNo').send_keys(contactPhoneNo)
                info_dict['contactPhoneNo'] = contactPhoneNo
                emailAddress = getEmail()
                self.driver.find_element_by_id('emailAddress').send_keys(emailAddress)
                info_dict['emailAddress'] = emailAddress
                self.driver.find_element_by_id('emailAddressRetype').send_keys(emailAddress)
                loginId = getLoginId()
                self.driver.find_element_by_id('loginId').send_keys(loginId)
                info_dict['loginId'] = loginId
                self.driver.find_element_by_id('password').send_keys('abcDEF123456')
                self.driver.find_element_by_id('passwordRetype').send_keys('abcDEF123456')
                info_list.append(info_dict)
                f.write(str(info_dict) + '\n')

                # 验证码
                # time.sleep(10)

                # 接受服务条款按钮
                self.driver.find_element_by_id('checkbox-tnc').click()
                # 点击确定按钮
                self.driver.find_element_by_xpath('//form/div/div/div[@id="button-confirm"]/div/div/span').click()
                # 判断是否注册成功
                try:
                    self.wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'confirmation-message')))
                    self.driver.find_element_by_class_name('confirmation-message')
                    if self.driver.find_element_by_class_name('confirmation-message'):
                        print('会员注册成功！')
                except Exception:
                    print("会员注册失败！")
        return info_list

    # 内容搜索
    def search(self):
        pass

    def runprogram(self):
        self.driver.get(self.url)
        # self.driver.maximize_window()
        # self.login()
        self.register()


if __name__ == '__main__':
    urbtix = CrawlUrbtix()
    urbtix.runprogram()

















