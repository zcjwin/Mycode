# coding: utf-8
import json
import configparser
import html.parser
import urllib, urllib.request, urllib.parse
import random


# 读取URL获得验证码的路径HTML解析类
import requests


class LoginRandCodeParser(html.parser.HTMLParser):
    def __init__(self):
        self.captchaurl = ""
        html.parser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'img' and ('id', 'captchaImage') in attrs:
            tag_attrs = dict(attrs)
            if 'src' in tag_attrs and tag_attrs['src']:
                # 登录验证码的相对路径
                # /internet/557/captchaImage.jpeg
                relative_path = tag_attrs['src']
                terms = str(relative_path).split('/')
                terms[2] = random.randint(40, 500)
                relative_path = '/' + terms[1] + '/' + str(terms[2]) + '/' + terms[3]
                # 完整路径
                self.captchaurl = "https://ticket.urbtix.hk" + relative_path


# 解析登录后返回的HTML, 获取用户帐户信息
# 用于判断用户是否成功登录
class InfoCenterParser(html.parser.HTMLParser):
    def __init__(self):
        self.session_time_left = ""
        self.is_session_time_left = False
        self.session_time = False
        html.parser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and ('id', 'session-time-left') in attrs:
            self.session_time = True
            self.is_session_time_left = True

    def handle_data(self, data):
        if self.session_time and self.is_session_time_left:
            self.session_time_left = data

    def handle_endtag(self, tag):
        if tag == 'div':
            self.session_time = False


class LogoutParser(html.parser.HTMLParser):
    def __init__(self):
        self.is_logout = False
        self.flag = False
        self.message = ''
        html.parser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and ('id', 'logout-page-intro') in attrs:
            self.is_logout = True
            self.flag = True

    def handle_data(self, data):
        # print(str(data).strip())
        if self.flag and self.is_logout:
            self.message = data

    def handle_endtag(self, tag):
        if tag == 'div':
            self.flag = False


# 获取验证码图片
def getRandImageUrl(ht):
    # 得到登录页面HTML内容
    # 必须先连到www.urbtix.hk,获取cookie，不能直接连ticket.urbtix.hk
    # loginHtml = ht.get(url="http://www.urbtix.hk/internet/en_US")
    loginHtml = ht.get(url="http://www.urbtix.hk/internet/zh_CN")
    loginHtml = ht.get(url="http://ticket.urbtix.hk/internet/login/member")
    loginHtml = ht.get(url="https://ticket.urbtix.hk/internet/login/member")
    # 解析登录页面内容，获取图片验证码的URL地址
    loginParer = LoginRandCodeParser()
    loginParer.feed(loginHtml)
    captchaurl = loginParer.captchaurl
    if captchaurl:
        return captchaurl
    else:
        f = open("login.html", 'w', encoding='utf-8')
        f.write(loginHtml)
        f.close()
        print("验证码URL获取失败, 详情查看返回的login.html页面")
    return None


def login(ht, username, password, captcha):
    post_data = {
        "j_username": username,
        "j_password": password,
        "captcha": captcha
    }
    # 用户登录，获取登录返回的HTML
    content = ht.post(url="https://ticket.urbtix.hk/internet/j_spring_security_check", params=post_data)
    content = ht.get(url='https://ticket.urbtix.hk/internet/')
    f = open("login_result.html", 'w', encoding='utf-8', errors='ignore')
    f.write(content)
    f.close()
    infocenterParser = InfoCenterParser()
    infocenterParser.feed(content)
    is_session_time_left = infocenterParser.is_session_time_left
    session_time_left = infocenterParser.session_time_left
    if is_session_time_left:
        print('登陆成功')
        print('session_time_left:', session_time_left)
        return True
    else:
        f = open("login_result.html", 'w', encoding='utf-8', errors='ignore')
        f.write(content)
        f.close()
        print("登录失败, 详情查看登录返回的login_result.html页面")

    return

def logout(ht):
    result = ht.get(url='https://ticket.urbtix.hk/internet/shoppingCart/checkEmpty')
    result = ht.post(url='https://ticket.urbtix.hk/internet/json/event/recentlyViewed/evt.json', params={})
    result = ht.get(url='https://ticket.urbtix.hk/internet/logout')
    f = open("logout_result.html", 'w', encoding='utf-8', errors='ignore')
    f.write(result)
    f.close()
    logoutP = LogoutParser()
    logoutP.feed(result)
    if logoutP.is_logout:
        message = logoutP.message
        print('logout message:', message)
    return logoutP.is_logout


# 读取config.ini文件获取用户设置的帐号信息
def getUserInfo():
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        username = config.get("UserInfo", "username")
        password = config.get("UserInfo", "password")
    except configparser.NoSectionError:
        print("请设置登录信息的config.ini文件")
        input("\r\n输入任意字符结束...")
    else:
        if username.strip() != '' and password.strip() != '':
            return (username, password)
        else:
            print("请设置登录的用户名与密码")
            input("\r\n输入任意字符结束...")

    return None


# 读取config.ini文件获取系统性配置信息
def getPerformanceInfo():
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        performanceInfo = dict(config.items("PerformanceInfo"))
        return performanceInfo
    except configparser.NoSectionError:
        print("系统性能配置装载失败!")
    return {}


def getGoAgentHost():
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        host = dict(config.items("GoAgentHost"))
        return host
    except configparser.NoSectionError:
        print("未设定代理服务器!")
    return {}
