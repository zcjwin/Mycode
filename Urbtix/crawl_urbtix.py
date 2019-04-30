import datetime
import sys,os
import time
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
from io import BytesIO
from random_userinfo import *
from fateadm_api import *
from ua import *

# filepath = './image/captcha/'+str(datetime.date.today())
# if not os.path.exists(filepath):
#     os.mkdir(filepath)






class CrawlUrbtix(object):
    def __init__(self):
        self.opt = webdriver.ChromeOptions()
        # self.opt.set_headless()
        # 创建浏览器对象
        self.driver = webdriver.Chrome(options=self.opt)
        # self.driver = webdriver.PhantomJS()
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        # self.url = 'http://msg.urbtix.hk/'
        self.url = 'http://www.urbtix.hk'

    def openfile(self):
        userinfo_list = []
        with open('infomation.txt',encoding='utf-8') as f:
            info_record = f.readlines()
            for record in info_record:
                info_rec_dic = eval(record)
                userinfo_list.append(info_rec_dic)
        message = random.choice(userinfo_list)
        self.login(message)

    def login(self,message):
        # filepath = os.mkdir(r'C:\Users\Administrator\Desktop\work\Urbtix\image' + str(datetime.date.today()))
        s = message
        # 点击登入到登录界面
        self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"登入")))
        self.driver.find_element_by_link_text('登入').click()
        try:
            if self.driver.find_element_by_class_name('ui-dialog'):
                self.driver.find_element_by_class_name('ui-dialog-buttonset').find_element_by_class_name('ui-button-text').click()
                print("每天 上午 09:40 (香港時間), 系統將會進行更新及只提供瀏覽模式 (登入 / 購票服務 暫停)。系統將於 上午 10:00 完成更新及恢復正常服務。")
                while (1):
                    t = time.strftime('%H:%M:%S', time.localtime(time.time()))
                    sys.stdout.write(t + '\b' * 10)
                    sys.stdout.flush()
                    time.sleep(0.1)
                    os.system('cls')
                    if t == "10:00:01":
                        break
                self.login(message)
        except NoSuchElementException:
            pass
        # 填写登录信息
        # self.driver.find_element_by_id('j_username').send_keys(s['loginId'])
        # self.driver.find_element_by_id('j_password').send_keys('abcDEF123456')

        self.driver.find_element_by_id('j_username').send_keys('zx18612015735')
        self.driver.find_element_by_id('j_password').send_keys('123456')

        # 验证码
        time.sleep(1)
        # 获取验证码图片
        currentpage = './image/screenshot/currentpage.png'
        self.driver.save_screenshot(currentpage)
        # 找到验证码元素的节点id
        captchaImage_element = self.driver.find_element_by_id('captchaImage')
        # print(captchaImage_element.location)  # 打印验证码元素的坐标位置
        # print(captchaImage_element.size)      # 打印验证码元素的大小
        left = captchaImage_element.location['x']
        top = captchaImage_element.location['y']
        right = captchaImage_element.location['x'] + captchaImage_element.size['width']
        bottom = captchaImage_element.location['y'] + captchaImage_element.size['height']
        # 找到验证码的位置并保存
        image = Image.open(currentpage)
        image = image.crop((left, top, right, bottom))
        image.save('./image/captcha/' + str(time.time()).replace('.', '') + '.png')
        image.save('./image/img/capatcha.png')

        t_captcha = self.driver.find_elements_by_xpath('//td[@id="captcha-image-input-key-container"]/table/tbody/tr/td')
        for i, img in enumerate(t_captcha):
            # print(img.location) # 每个点击验证码的坐标位置
            left = img.location['x']
            top = img.location['y']
            right = img.location['x'] + img.size['width']
            bottom = img.location['y'] + img.size['height']
            img = Image.open(currentpage)
            img = img.crop((left, top, right, bottom))
            img.save('./image/clickimg/' + str(time.time()).replace('.','') + '.png')
            img.save('./image/img/' + str(i) + '.png')

        ss = TestFunc(file_dir="./image/img")
        for i in range(len(ss[-1])):
            for j, s in enumerate(ss):
                if s == ss[-1][i]:
                    t_captcha[j].click()
        # input_captcha = self.driver.find_element_by_id('captcha-image-input-key-selected-container')
        # tr = input_captcha.find_element_by_tag_name('table').find_element_by_id('tbody').find_element_by_tag_name('tr')
        # td = tr.find_elements_by_tag_name('td')
        # print(ss)
        # if not td:
            # 点击登入按钮
        time.sleep(2)
        self.driver.find_element_by_class_name('btn-inner-blk').click()
        try:
            login_eeror = self.driver.find_element_by_class_name('login-error')
            if login_eeror:
                self.login(message)
        except NoSuchElementException:
            dr = self.driver.find_elements_by_class_name('mem-login-state-link')[0].text
            if dr == "登出":
                print("登录成功！")
                self.search()
            else:
                if self.driver.find_element_by_id('concurrent-login-yes'):
                    self.driver.find_element_by_id('concurrent-login-yes').click()
                    self.search()
                else:
                    self.login(message)
                self.login(message)


    # 注册信息界面
    def register(self):
        info_list = []
        with codecs.open('infomation.txt','a+','utf-8') as f:
            infocount = int(input("请输入您要随机生成的注册信息数量："))
            for count in range(infocount):
                info_dict = {}
                self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"登入")))
                self.driver.find_element_by_link_text('登入').click()
                # 等待继续按钮元素加载完再执行点击
                try:
                    self.wait.until(EC.visibility_of_element_located(
                        (By.XPATH,'//table/tbody/tr/td/div/div/div[@class="member-login-become-member"]/div/div/span')))
                except TimeoutException:
                    print("请稍等...")
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

                # 验证码
                # time.sleep(10)
                currentpage = './image/screenshot/currentpage.png'
                self.driver.save_screenshot(currentpage)
                # 找到验证码元素的节点id
                captchaImage_element = self.driver.find_element_by_id('captchaImage')
                # print(captchaImage_element.location)  # 打印验证码元素的坐标位置
                # print(captchaImage_element.size)      # 打印验证码元素的大小
                left = captchaImage_element.location['x']
                top = captchaImage_element.location['y']
                right = captchaImage_element.location['x'] + captchaImage_element.size['width']
                bottom = captchaImage_element.location['y'] + captchaImage_element.size['height']
                # 找到验证码的位置并保存
                image = Image.open(currentpage)
                image = image.crop((left, top, right, bottom))
                image.save('./image/captcha/' + str(time.time()).replace('.', '') + '.png')
                image.save('./image/img/capatcha.png')

                t_captcha = self.driver.find_elements_by_xpath(
                    '//td[@id="captcha-image-input-key-container"]/table/tbody/tr/td')
                for i, img in enumerate(t_captcha):
                    # print(img.location) # 每个点击验证码的坐标位置
                    left = img.location['x']
                    top = img.location['y']
                    right = img.location['x'] + img.size['width']
                    bottom = img.location['y'] + img.size['height']
                    img = Image.open(currentpage)
                    img = img.crop((left, top, right, bottom))
                    img.save('./image/clickimg/' + str(time.time()).replace('.', '') + '.png')
                    img.save('./image/img/' + str(i) + '.png')

                # ss = TestFunc(file_dir="./image/img")
                # for i in range(len(ss[-1])):
                #     for j, s in enumerate(ss):
                #         if s == ss[-1][i]:
                #             t_captcha[j].click()

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
                        info_list.append(info_dict)
                        f.write(str(info_dict) + '\n')
                except Exception:
                    print("会员注册失败！")
        return info_list

    # 内容搜索
    def search(self):
        keyword = input("请输入您要搜索的演出：")
        self.driver.find_element_by_id('adv-srch-txt').send_keys(keyword)
        self.driver.find_element_by_id('adv-srch-img').click()
        try:
            # 演出时间
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'event-date-col')))
            dateobj = self.driver.find_elements_by_class_name('event-date-col')
            # 节目名称
            self.wait.until(EC.presence_of_element_located((
                By.XPATH, '//table/tbody/tr/td[@class="event-eventname-col"]/a'
            )))
            pronameobj = self.driver.find_elements_by_xpath('//table/tbody/tr/td[@class="event-eventname-col"]/a')
            # 演出地点
            self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH, '//table[@id="event-list-tbl"]/tbody/tr/td[@class="event-venuename-col"]'
                ))
            )
            addressobj = self.driver.find_elements_by_xpath(
                '//table[@id="event-list-tbl"]/tbody/tr/td[@class="event-venuename-col"]')
            # 票价
            self.wait.until(EC.presence_of_element_located((
                By.XPATH, '//table[@id="event-list-tbl"]/tbody/tr/td[@class="event-ticket-price-col"]/div'
            )))
            priceobj = self.driver.find_elements_by_xpath(
                '//table[@id="event-list-tbl"]/tbody/tr/td[@class="event-ticket-price-col"]/div')

            # 显示演出的时间、地点、名称、票价
            print('+' * 80)
            for i, date, proname, address, price in zip([i + 1 for i in range(len(dateobj))], dateobj, pronameobj,
                                                        addressobj, priceobj):
                print(i, '、|', date.text, '|', proname.text, '|', address.text, '|', price.text)
                print('+' * 80)
            c = int(input("请选择节目名称序号："))
            self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH, '//table/tbody/tr/td/div/div[@class="btn-inner-blk"]/span'
                ))
            )
            self.driver.find_element_by_xpath(
                '//table/tbody/tr[' + str(c + 1) + ']/td/div/div[@class="btn-inner-blk"]/span').click()
        except NoSuchElementException as ex:
            print(ex)

        # 选择场次
        # self.wait.until(EC.presence_of_element_located((
        #     By.XPATH,
        #     '//table[@id="evt-perf-items-tbl"]/tbody/tr/td/div/div'
        # )))
        perfmonth = self.driver.find_elements_by_xpath('//table[@id="evt-perf-items-tbl"]/tbody/tr/td/div/div[1]')
        perfdate = self.driver.find_elements_by_xpath('//table[@id="evt-perf-items-tbl"]/tbody/tr/td/div/div[2]')
        perfday = self.driver.find_elements_by_xpath('//table[@id="evt-perf-items-tbl"]/tbody/tr/td/div/div[3]')
        perfyear = self.driver.find_elements_by_xpath('//table[@id="evt-perf-items-tbl"]/tbody/tr/td/div/div[4]')
        perftime = self.driver.find_elements_by_xpath('//table[@id="evt-perf-items-tbl"]/tbody/tr/td[2]/span')
        perfname = self.driver.find_elements_by_xpath('//table[@id="evt-perf-items-tbl"]/tbody/tr/td[3]')
        for i, month, date, day, year, ptime, name in zip([i + 1 for i in range(len(perftime))],
                                                          perfmonth, perfdate, perfday, perfyear, perftime, perfname):
            print(i, '、|', month.text, date.text, day.text, year.text, ptime.text, '|', name.text)

        # 点击购买门票
        p = int(input("请选择您要节目场次："))
        buy_element = self.driver.find_elements_by_class_name('event-buy-status-col')
        if buy_element[p-1].text:
            print("售罄")
            input("按任意键重新搜索...")
            self.search()
        else:
            buy_element[p-1].click()
            # 选择购买正价票数量
            selector = Select(self.driver.find_element_by_id('ticket-quota-223-sel'))
            # 下拉框票最大数量
            sn = self.driver.find_elements_by_xpath(
                '//table[@id="ticket-type-tbl"]/tbody/tr[1]/td[@class="ticket-type-quota"]/select/option')
            print("允许购买最多票数：", len(sn)-1)
            n = int(input("请输入您要购买票的数量："))
            selector.select_by_value(str(n))
            # selector.select_by_visible_text('2')
            self.driver.find_element_by_class_name('btn-inner-blk').click() # 快速购买
            # 如果出现系統未能於所選區段選取相連座位，如您選擇"確定"，系統會重試不相連座位。点击确定
            try:
                self.driver.find_element_by_class_name('ui-dialog') #prompt_dialog =
            # if prompt_dialog:
                dialog_button = self.driver.find_element_by_class_name('ui-dialog-buttonset')
                choose_button = dialog_button.find_elements_by_class_name('ui-button-text-only')
                choose_button[0].find_element_by_class_name('ui-button-text').click()   # 确定
                try:
                    self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'ticket-review-seats-123436-tbl')))
                except TimeoutException:
                    time.sleep(2)
                self.driver.find_element_by_id('checkbox-not-adjacent').click()
                # 点击加入购物篮
                self.driver.find_element_by_xpath('//form[@id="reviewTicketForm"]/div/div/div[@class="btn-inner-blk"]/span').click()
                # 点击往付款区
                self.driver.find_element_by_xpath(
                    '//form/table/tbody/tr/td/div[@id="checkout-btn"]/div/div[@class="btn-inner-blk"]/span').click()
                # 选择取票方式设置为自动取票机取票
                get_ticket_way = Select(self.driver.find_element_by_id('delivery-method-select'))
                get_ticket_way.select_by_index(1)
                # 选择付款方法
                self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME,'ddTitleText'))
                )
                payment_way = self.driver.find_element_by_class_name('ddTitleText').click()
                choose_pay = self.driver.find_element_by_id('payment-type-select_child')
                enable_pay = choose_pay.find_element_by_tag_name('ul')
                pay = enable_pay.find_elements_by_tag_name('li')
                pay[2].click()  # 万事达卡

                self.driver.find_element_by_id('input-card-number').send_keys('5308171895071873')
                self.driver.find_element_by_id('input-security-code').send_keys('123')
                # 选择卡号有效日期
                effective_month = Select(self.driver.find_element_by_id('payment-expiry-month-select'))
                effective_month.select_by_visible_text('08')
                effective_year = Select(self.driver.find_element_by_id('payment-expiry-year-select'))
                effective_year.select_by_visible_text('2028')
                self.driver.find_element_by_xpath('//form/div/div/div/div[@id="button-confirm"]/div/div/span').click()
                self.driver.find_element_by_id('checkbox-tnc').click()
                self.driver.find_element_by_xpath('//form/div/div/div[@id="button-confirm"]/div/div/span').click()
            except NoSuchElementException:
                self.driver.find_element_by_xpath(
                    '//form[@id="reviewTicketForm"]/div/div/div[@class="btn-inner-blk"]/span').click()
                # 点击往付款区
                self.driver.find_element_by_xpath(
                    '//form/table/tbody/tr/td/div[@id="checkout-btn"]/div/div[@class="btn-inner-blk"]/span').click()
                # 选择取票方式设置为自动取票机取票
                get_ticket_way = Select(self.driver.find_element_by_id('delivery-method-select'))
                get_ticket_way.select_by_index(1)
                # 选择付款方法
                self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'ddTitleText'))
                )
                payment_way = self.driver.find_element_by_class_name('ddTitleText').click()
                choose_pay = self.driver.find_element_by_id('payment-type-select_child')
                enable_pay = choose_pay.find_element_by_tag_name('ul')
                pay = enable_pay.find_elements_by_tag_name('li')
                pay[2].click()  # 万事达卡
                card_num = input("请输入您要付款的银行卡账号：")
                self.driver.find_element_by_id('input-card-number').send_keys('5308171895071873')
                self.driver.find_element_by_id('input-security-code').send_keys('123')
                # 选择卡号有效日期
                effective_month = Select(self.driver.find_element_by_id('payment-expiry-month-select'))
                effective_month.select_by_visible_text('08')
                effective_year = Select(self.driver.find_element_by_id('payment-expiry-year-select'))
                effective_year.select_by_visible_text('2028')
                self.driver.find_element_by_xpath('//form/div/div/div/div[@id="button-confirm"]/div/div/span').click()
                self.driver.find_element_by_id('checkbox-tnc').click()
                self.driver.find_element_by_xpath('//form/div/div/div[@id="button-confirm"]/div/div/span').click()
                # 判断是否付款成功
                try:
                    self.driver.find_element_by_class_name('')
                except NoSuchElementException:
                    print("购买失败!")
                    self.search()


    def start(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

        print('+' * 23)
        print('|' + ' ' * 5 + '1、登录账户' + ' ' * 5 + '|')
        print('|' + ' ' * 5 + '2、注册账户' + ' ' * 5 + '|')
        print('+' * 23)
        n = int(input("请选择："))
        L = [1, 2]
        if n not in L:
            int(input("请输入正确的序号："))
        if n == 1:
            self.openfile()
        if n == 2:
            self.register()


if __name__ == '__main__':
    urbtix = CrawlUrbtix()
    urbtix.start()

















