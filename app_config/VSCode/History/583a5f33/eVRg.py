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


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# os.system('start Chrome --remote-debugging-port=9222')
# os.system('/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222')

options = Options()
options.add_argument('--remote-debugging-port=9222')
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
browser.get('https://www.zhihu.com/signin')



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