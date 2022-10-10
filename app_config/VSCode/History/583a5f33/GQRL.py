# -*- coding: utf-8 -*-

# https://www.programminghunter.com/article/70742032165/

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib
from urllib import parse
from xml.sax.saxutils import unescape,escape
import datetime,time

# Default header
DEFAULT_REQUEST_HEADERS = {
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Referer': 'https://www.zhihu.com/',
}

login_header = {
    "content-type": "application/x-www-form-urlencoded",
    "x-zse-83": "3_1.1",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Referer': 'https://www.zhihu.com',
    'HOST': 'www.zhihu.com',
    ':authority': 'www.zhihu.com'
}


config_setting = {
    "ACCOUNT_USERNAME": "",
    "ACCOUNT_PASSWORD": ""
}

class login_ZhiHuSpider():

    name = "zhihu"
    start_urls = ['https://zhihu.com']
    allowed_domains = ['www.zhihu.com']
    headers = DEFAULT_REQUEST_HEADERS
    # 每个问题获取遍历多少个答案
    username = config_setting['ACCOUNT_USERNAME']
    password = config_setting['ACCOUNT_PASSWORD']
    cookies = {}
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    def start_requests(self):
        records = []
        item = {}
        driver = webdriver.Chrome(chrome_options=self.chrome_options)
        print(driver.title)
        url = "https://www.zhihu.com/signin?next=%2F"
        driver.get(url)
        netloc = parse.urlparse(url).netloc
        print(netloc)
        if self.username != '':
            driver.find_element_by_xpath("//*[@name='username']").send_keys(self.username)

        if self.password != '':
            driver.find_element_by_xpath("//*[@name='password']").send_keys(self.password)

        input('请在浏览器上登陆后，请点击按任意键开始：')

        print("测试环节，建议手动在调试浏览器输入账号密码，看能否成功")
        ##driver.close()
        # 翻页请求问题相关
if __name__ == "__main__":
    login_ZhiHuSpider().start_requests()