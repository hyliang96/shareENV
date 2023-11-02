from http import server
from optparse import Option
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# service=Service(ChromeDriverManager().install())
service=Service('./chromedriver')

from selenium.webdriver.chrome.options import Options
import threading
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from xml import etree

def normal_chrome():
    os.system('/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222')

def is_not_presence(driver, locator, timeout=10):
    try:
        WebDriverWait(driver, timeout).until_not(EC.presence_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

def main():
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=service ,options=options)
    driver.get('https://www.zhihu.com/signin')

    # elem = driver.find_element(By.LINK_TEXT,'我的主页')
    # elem.click()

    # import requests
    # s = requests.Session()
    # selenium_user_agent = driver.execute_script("return navigator.userAgent;")
    # s.headers.update({"user-agent": selenium_user_agent})
    # for cookie in driver.get_cookies():
    #     s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

    # # 发起访问请求
    # r = s.get('https://www.zhihu.com/people/lao-liang-83-95/posts')
    # print(r)

    driver.get(f'https://www.zhihu.com/people/lao-liang-83-95/posts')
    page_ids = driver.find_elements(By.XPATH,'(//button[@class="Button PaginationButton PaginationButton--current Button--plain"])')
    page_ids += driver.find_elements(By.XPATH,'(//button[@class="Button PaginationButton Button--plain"])')
    page_num=max([int(page_id.text) for page_id in page_ids])
    print('page_num=', page_num)

    titles, urls = [], []
    for page_id in range(1,page_num+1):
        time.sleep(10)
        driver.get(f'https://www.zhihu.com/people/lao-liang-83-95/posts?page={page_id}')

        # with open('post1.html', 'w') as f:
            # f.write(driver.page_source)
        # break

        plcaeholder = driver.find_elements(By.XPATH, '(//div[@class="PlaceHolder List-item"])')
        print('plcaeholder', plcaeholder)

        is_not_presence(driver, '(//div[@class="PlaceHolder List-item"])', timeout=10)

        # try:
        #     WebDriverWait(driver, 20).until_not(
        #         EC.presence_of_element_located((By.XPATH, '(//div[@class="PlaceHolder List-item"])'))
        #     )
        # finally:
        #     print('time out')
        #     # driver.quit()


        # time.sleep(10)

        item_titles = driver.find_elements(By.XPATH,'(//h2[@class="ContentItem-title"]//a)')
        item_urls = driver.find_elements(By.XPATH,'(//h2[@class="ContentItem-title"]//a[@href])')
        print('num(item_titles)=', len(item_titles))
        print('num(item_urls)', len(item_urls))
        for ind,i in enumerate(item_urls):
            title = item_titles[ind].text
            url = item_urls[ind].get_attribute('href')
            titles.append(title)
            urls.append(url)
            # print(title, url, len(titles), len(urls))

    # ProfileMain-header
    # elem = driver.find_element(By.LINK_TEXT,'https://www.zhihu.com/people/lao-liang-83-95/posts')

    # elem = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[3]/div[1]/div/div[1]/ul/li[5]/a') # 文章
    # elem.click()

    for article_id, (title, url) in enumerate(zip(titles, urls)):
        print(article_id+1, title, url)

    # https://blog.csdn.net/weixin_47163937/article/details/115330332
    # for title, url in zip(titles, urls):
    #     article_id = url.split('/')[-1]
    #     driver.get(url)
    #     html = etree.HTML(driver.page_source)
    #     txt = '\n'.join(html.xpath('//*[@id="root"]/div/main/div/article/div[1]//text()'))
    #     with open(f"./article/{title}-{article_id}.txt", "w", encoding="utf-8") as f:
    #         f.write(txt)
    #     break

    driver.close()
    driver.quit()

t1=threading.Thread(target=normal_chrome)
t2=threading.Thread(target=main)

t1.start()
t2.start()

t1.join()
t2.join()

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
