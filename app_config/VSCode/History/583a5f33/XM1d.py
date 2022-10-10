# https://3yya.com/lesson/66


import os

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

os.system('PATH="/Applications/Google Chrome.app/Contents/MacOS:$PATH" Google\ Chrome --remote-debugging-port=9222')

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

browser = webdriver.Chrome(options=options)
browser.get('https://www.zhihu.com/signin')

input('登录完成后回车：')
print(browser.get_cookies())