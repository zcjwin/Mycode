import random

from selenium import webdriver
import time
import requests
import multiprocessing
from threading import Thread

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from .random_userinfo import *
from selenium.common.exceptions import NoSuchElementException
# from Urbtix.proxy import *
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def urbtix_login():
    opt = webdriver.ChromeOptions()
    # opt.set_headless()
    opt.add_argument(
        'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
    # 创建浏览器对象
    driver = webdriver.Chrome(options=opt)
    # url = 'http://msg.urbtix.hk/'
    url = 'http://www.urbtix.hk'
    driver.get(url)
    # driver.maximize_window()
    with open('infomation.txt', encoding='utf-8') as file_obj:
        contents = file_obj.read()
        con = contents.splitlines()
        for c in con:
            s = eval(c)
            # 等待页面加载出现"登入"
            WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.LINK_TEXT, "登入")))
            driver.find_element_by_link_text('登入').click()

            if driver.find_element_by_class_name('ui-dialog'):
                driver.find_element_by_class_name('ui-dialog-buttonset').find_element_by_class_name('ui-button-text').click()
                urbtix_login()
            else:
                dr = driver.find_elements_by_class_name('mem-login-state-link')[0].text
                if dr == "登出":
                    print("登录成功！")
                    search()
                elif driver.find_element_by_id('concurrent-login-yes'):
                    driver.find_element_by_id('concurrent-login-yes').click()
                    search()

            driver.find_element_by_id('j_username').send_keys(s['loginId'])
            driver.find_element_by_id('j_password').send_keys(s['abcDEF123456'])
            # 验证码
            time.sleep(5)
            driver.find_element_by_class_name('btn-inner-blk').click()
            try:
                if driver.find_element_by_class_name('mem-login-state-link'):
                    print('登录成功！')
                    search()
            except Exception:
                print('登录失败！')


def urbtix_register():
    opt = webdriver.ChromeOptions()
    # opt.set_headless()
    # 设置代理ip
    # url = 'https://www.kuaidaili.com/free/'
    # ip_list = get_ip_list(url)
    # proxies = get_random_ip(ip_list)
    # opt.add_argument('--proxy-server='+proxies)
    # 创建浏览器对象
    driver = webdriver.Chrome(options=opt)
    # url = 'http://msg.urbtix.hk/'
    url = 'http://www.urbtix.hk'
    driver.get(url)
    # driver.maximize_window()

    with open('infomation.txt', encoding='utf-8') as file_obj:
        contents = file_obj.read()
        con = contents.splitlines()
        for c in con:
            s = eval(c)
            # 等待页面加载出现"登入"
            WebDriverWait(driver,10,0.5).until(EC.visibility_of_element_located((By.LINK_TEXT,"登入")))
            driver.find_element_by_link_text('登入').click()
            # 点击"继续"到注册页面
            driver.find_element_by_xpath('//table/tbody/tr/td/div/div/div[@class="member-login-become-member"]/div/div/span').click()
            # 填写注册信息
            driver.find_element_by_id('surname').send_keys(s['surname'])
            driver.find_element_by_id('firstName').send_keys(s['firstName'])
            driver.find_element_by_id('contactPhoneNo').send_keys(s['contactPhoneNo'])
            driver.find_element_by_id('emailAddress').send_keys(s['emailAddress'])
            driver.find_element_by_id('emailAddressRetype').send_keys(s['emailAddress'])
            driver.find_element_by_id('loginId').send_keys(s['loginId'])
            driver.find_element_by_id('password').send_keys('abcDEF123456')
            driver.find_element_by_id('passwordRetype').send_keys('abcDEF123456')
            # 验证码
            time.sleep(10)
            # 点击接受服务条款按钮
            driver.find_element_by_id('checkbox-tnc').click()
            # 确定
            driver.find_element_by_xpath('//form[@id="memberSignUpForm"]/div/div/div[@id="button-confirm"]/div/div/span').click()
            # 判断是否注册成功
            try:
                WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME,'confirmation-message')))
                driver.find_element_by_class_name('confirmation-message')
                if driver.find_element_by_class_name('confirmation-message'):
                    print('会员注册成功！')
            except Exception:
                print("会员注册失败！")

def search():
    opt = webdriver.ChromeOptions()
    # opt.set_headless()
    # 创建浏览器对象
    driver = webdriver.Chrome(options=opt)
    url = 'http://www.urbtix.hk'
    driver.get(url)
    keyword = input("请输入您要搜索的演出：")
    driver.find_element_by_id('adv-srch-txt').send_keys(keyword)
    driver.find_element_by_id('adv-srch-img').click()
    try:
        # 演出时间
        WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.CLASS_NAME,'event-date-col')))
        dateobj = driver.find_elements_by_class_name('event-date-col')
        # 节目名称
        WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((
            By.XPATH,'//table/tbody/tr/td[@class="event-eventname-col"]/a'
        )))
        pronameobj = driver.find_elements_by_xpath('//table/tbody/tr/td[@class="event-eventname-col"]/a')
        # 演出地点
        WebDriverWait(driver, 10, 0.5).until(
            EC.presence_of_element_located((
                By.XPATH, '//table[@id="event-list-tbl"]/tbody/tr/td[@class="event-venuename-col"]'
            ))
        )
        addressobj = driver.find_elements_by_xpath('//table[@id="event-list-tbl"]/tbody/tr/td[@class="event-venuename-col"]')
        # 票价
        WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((
            By.XPATH, '//table[@id="event-list-tbl"]/tbody/tr/td[@class="event-ticket-price-col"]/div'
        )))
        priceobj = driver.find_elements_by_xpath('//table[@id="event-list-tbl"]/tbody/tr/td[@class="event-ticket-price-col"]/div')

        # 显示演出的时间、地点、名称、票价
        print('+' * 80)
        for i, date, proname, address, price in zip([i+1 for i in range(len(dateobj))],dateobj,pronameobj,addressobj, priceobj):
            print(i,'、|',date.text,'|',proname.text,'|',address.text,'|',price.text)
            print('+' * 80)
        c = int(input("请选择演出序号："))
        WebDriverWait(driver,10,0.5).until(
            EC.presence_of_element_located((
                By.XPATH,'//table/tbody/tr/td/div/div[@class="btn-inner-blk"]/span'
            ))
        )
        driver.find_element_by_xpath('//table/tbody/tr['+str(c+1)+']/td/div/div[@class="btn-inner-blk"]/span').click()
    except Exception as e:
        print(e)
    except NoSuchElementException as ex:
        print(ex)

    # 选择场次
    WebDriverWait(driver,10,05.).until(EC.presence_of_element_located((
        By.XPATH,'//table[@id="evt-perf-items-tbl"]/tbody/tr/td[@class="perf-cal-col"]/div[@class="perf-cal-div"]/div'
    )))
    perfmonth = driver.find_elements_by_xpath( '//table[@id="evt-perf-items-tbl"]/tbody/tr/td/div/div[1]')
    perfdate = driver.find_elements_by_xpath( '//table[@id="evt-perf-items-tbl"]/tbody/tr/td/div/div[2]')
    perfday = driver.find_elements_by_xpath( '//table[@id="evt-perf-items-tbl"]/tbody/tr/td/div/div[3]')
    perfyear = driver.find_elements_by_xpath( '//table[@id="evt-perf-items-tbl"]/tbody/tr/td/div/div[4]')
    perftime = driver.find_elements_by_xpath('//table[@id="evt-perf-items-tbl"]/tbody/tr/td[2]/span')
    perfname = driver.find_elements_by_xpath('//table[@id="evt-perf-items-tbl"]/tbody/tr/td[3]')
    for i,month,date,day,year, ptime, name in zip([i + 1 for i in range(len(perftime))],
                             perfmonth,perfdate,perfday,perfyear,perftime, perfname):
        print(i,'、|',month.text,date.text,day.text,year.text,ptime.text,'|',name.text)

    # 点击购买门票
    WebDriverWait(driver, 10,0.5).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, 'event-buy-status-col'
        ))
    )
    p = int(input("请选择您要节目场次："))
    WebDriverWait(driver, 10, 0.5).until(
        EC.presence_of_element_located((
            By.XPATH, '//table[@id="evt-perf-items-tbl"]/tbody/tr[' + str(p) + ']/td[@class="perf-purchase-col"]/div[@class="event-buy-status-col"]/img'
        ))
    )
    driver.find_element_by_xpath('//table[@id="evt-perf-items-tbl"]/tbody/tr['+str(p)+']/td[@class="perf-purchase-col"]/div[@class="event-buy-status-col"]/img').click()
    # 选择购买正价票数量
    selector = Select(driver.find_element_by_id('ticket-quota-223-sel'))
    # 下拉框票最大数量
    sn = driver.find_elements_by_xpath(
        '//table[@id="ticket-type-tbl"]/tbody/tr[1]/td[@class="ticket-type-quota"]/select')
    print("允许购买最多票数：", len(sn))
    n = int(input("请输入您要购买票的数量："))
    selector.select_by_value(str(n))
    # selector.select_by_visible_text('2')
    # 如果出现系統未能於所選區段選取相連座位，如您選擇"確定"，系統會重試不相連座位。点击确定
    if driver.find_element_by_class_name(
            'ui-dialog ui-widget ui-widget-content ui-corner-all ui-front ui-dialog-buttons ui-draggable'):
        driver.find_element_by_class_name('ui-button-text').click()
    # 点击快速购票
    driver.find_element_by_xpath(
        '//form[@id="performanceSelectForm"]/div/div/div[@id="express-purchase-btn"]/div[@class="btn-inner-blk"]/span').click()
    # 点击加入购物车
    driver.find_element_by_xpath('//form[@id="reviewTicketForm"]/div/div/div[@class="btn-inner-blk"]/span').click()
    # 点击往付款区
    driver.find_element_by_xpath(
        '//form/table/tbody/tr/td/div[@id="checkout-btn"]/div/div[@class="btn-inner-blk"]/span').click()
    # 选择取票方式设置为自动取票机取票
    get_ticket_way = Select(driver.find_element_by_id('delivery-method-select'))
    get_ticket_way.select_by_index(1)
    # 选择付款方法
    payment_way = Select(driver.find_element_by_id('payment-type-select_title'))
    payment_way.select_by_index(2)
    driver.find_element_by_id('input-card-number').send_keys('5308171895071873')
    driver.find_element_by_id('input-security-code').send_keys('123')
    # 选择卡号有效日期
    effective_month = Select(driver.find_element_by_id('payment-expiry-month-select'))
    effective_month.select_by_index(0)
    effective_year = Select(driver.find_element_by_id('payment-expiry-year-select'))
    effective_year.select_by_index(0)
    driver.find_element_by_xpath('//form/div/div/div/div[@id="button-confirm"]/div/div/span').click()
    driver.find_element_by_id('checkbox-tnc').click()
    driver.find_element_by_xpath('//form/div/div/div[@id="button-confirm"]/div/div/span').click()

def main():
    print('+' * 23)
    print('|' + ' ' * 5 + '1、注册账户' + ' ' * 5 + '|')
    print('|' + ' ' * 5 + '2、登录账户' + ' ' * 5 + '|')
    print('|' + ' ' * 5 + '3、节目搜索' + ' ' * 5 + '|')
    print('+' * 23)
    n = int(input("请选择："))
    L = [1,2,3]
    if n not in L:
        int(input("请输入正确的序号："))
    if n == 1:
        urbtix_register()
    if n == 2:
        urbtix_login()
    if n == 3:
        search()



if __name__ == "__main__":
    main()



