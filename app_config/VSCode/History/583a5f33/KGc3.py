import os

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

os.system('start Chrome --remote-debugging-port=9222')

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

browser = webdriver.Chrome(options=options)
browser.get('https://www.zhihu.com/signin')