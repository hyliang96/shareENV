# https://3yya.com/lesson/66

# https://www.gairuo.com/p/python-selenium

from selenium import webdriver
from selenium.webdriver import FirefoxOptions

opts = FirefoxOptions()
opts.add_argument("--headless") # 无头浏览器

# browser = webdriver.Chrome()
browser = webdriver.Firefox(options=opts)
# 指定浏览器驱动
b = webdriver.Firefox(executable_path='./geckodriver')

browser.get('https://www.baidu.com')
browser.page_source # 输出源码
browser.title # 网页标量
browser.close()
browser.quit()