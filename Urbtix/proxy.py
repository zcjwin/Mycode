from bs4 import BeautifulSoup
import requests
import random
import urllib
ip_list=[]

def get_ip_list(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
    for i in range(10,30):           #设置页数，这里设置10到30页
        i=str(i)
        url_c=url+'/inha/'+i+'/'
        web_data = requests.get(url,headers=headers)
        soup = BeautifulSoup(web_data.text, 'html.parser')
        ips = soup.find_all('tr')
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[0].text+':'+tds[1].text)       #ip加端口号
        #检测ip可用性，移除不可用ip
    for ip in ip_list:
        try:
          proxy_host = "https://" + ip
          proxy_temp = {"https": proxy_host}
          res = urllib.urlopen(url, proxies=proxy_temp).read()           #访问一个网站，看看是否返回200
        except Exception as e:
          ip_list.remove(ip)                  #去除无效的ip
          continue
    return ip_list

def get_random_ip(ip_list):          #在ip池中随机取一个ip使用
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    # proxies = {'http': proxy_ip}
    # return proxies
    return proxy_ip


if __name__ == '__main__':
    url = 'https://www.kuaidaili.com/free/'
    ip_list = get_ip_list(url)
    proxies = get_random_ip(ip_list)
    # print(ip_list)
    print(proxies)

