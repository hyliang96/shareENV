from optparse import Option
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# service=Service(ChromeDriverManager().install())

from selenium.webdriver.chrome.options import Options

import os

os.system('/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222')
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)

driver.get('https://www.zhihu.com/signin')


# https://3yya.com/lesson/66

# https://www.gairuo.com/p/python-selenium

# https://itsmycode.com/executable-path-has-been-deprecated/

# from selenium import webdriver
# from selenium.webdriver import FirefoxOptions
# from selenium.webdriver.chrome.service import Service


# opts = FirefoxOptions()
# opts.add_argument("--headless") # 无头浏览器

# # browser = webdriver.Chrome()
# s=Service('./geckodriver')
# browser = webdriver.Firefox(service=s, options=opts)
# # 指定浏览器驱动
# # b = webdriver.Firefox(executable_path='/Users/mac/Desktop/知乎/geckodriver')


# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# import os
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver

# # os.system('start Chrome --remote-debugging-port=9222')
# # os.system('/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222')

# options = Options()
# # options.add_argument('--remote-debugging-port=9222')
# # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver.get('https://www.zhihu.com/signin?next=%2F')

# # https://blog.csdn.net/Rebacca122222/article/details/123843492
# from selenium.webdriver.common.keys import Keys
# import time

# time.sleep(1)
# #点击密码登录界面
# driver.find_element_by_css_selector("div[class='SignFlow-tab']").click()
# #找到用户框，输入用户名

# elem=driver.find_element_by_name("username")
# elem.clear()
# #输入账号
# elem.send_keys("1788825778")
# #找到密码框，输入密码
# password=driver.find_element_by_name("password")
# password.clear()

# password.send_keys("yhl1328zh")
# #
# ##模拟键盘回车
# elem.send_keys(Keys.RETURN)
# time.sleep(4)
# print(driver.page_source)
# driver.quit()


# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.expected_conditions import presence_of_element_located

# import requests
# from fake_useragent import UserAgent
# #This example requires Selenium WebDriver 3.13 or newer

# browser.get('https://www.zhihu.com/signin')

# input('登录完成后回车：')

# cookies = {item['name']: item['value'] for item in browser.get_cookies()}

# ua = UserAgent()

# response = requests.get(
#     'https://www.zhihu.com/api/v3/feed/topstory/recommend?page_number=4&after_id=17',
#     headers={'User-Agent': ua.random},
#     cookies=cookies,
# )

# print(response.status_code)
# print(response.text)