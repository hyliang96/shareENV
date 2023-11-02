#--------------------------------------
# config
#--------------------------------------
# user_id='lao-liang-83-95'
save_dir = '../zhihu_backup/html'
chrome_log = 'chrome_log'
driver_path = './chromedriver'
#--------------------------------------
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from lxml import etree
import signal
import subprocess
import requests
import re
import json

from contextlib import contextmanager
@contextmanager
def suppress_output():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

with suppress_output():
    from webdriver_manager.chrome import ChromeDriverManager
#--------------------------------------
here = os.path.dirname(os.path.realpath(__file__)) # get absoltae path to the dir this file is in
save_dir = os.path.join(here, save_dir)
chrome_log = os.path.join(here, chrome_log)
driver_path = os.path.join(here, driver_path)
#--------------------------------------
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
}

class NormalChrome(object):
    def __init__(self,chrome_log):
        self.log = open(chrome_log, 'w')
        process = subprocess.Popen('/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222',
            stdout=self.log, stderr=self.log, shell=True)
        self.pid = process.pid
    def close(self):
        self.log.close()
        os.kill(self.pid, signal.SIGKILL)

def wait_until(driver, locator, timeout=10, until_not=False):
    try:
        if until_not:
            WebDriverWait(driver, timeout).until_not(EC.presence_of_element_located((By.XPATH, locator)))
        else:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

def start_driver(driver_path):
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_argument('--log-level=3')

    service=Service(ChromeDriverManager().install())

    # service=Service(driver_path)
    driver = webdriver.Chrome(service=service ,options=options) #  service_log_path=chrome_log
    return driver

def login_zhihu(driver):
    not_logged = False
    for i in range(60):
        driver.get('https://www.zhihu.com/signin')
        button_xpath = '(//button[@id="Popover15-toggle"])'
        if not wait_until(driver, button_xpath, timeout=5):
            if i == 0:
                print(
'''若无之前登录知乎的缓存, 请手动登录知乎:
在当前打开的浏览器内新建一个标签页
访问https://zhuanlan.zhihu.com/signin
手动填写账号, 密码, 验证码

...等待登陆''')
                not_logged = True
            continue
        else:
            print('已登录知乎')
            if not_logged:
                print('可关闭手动登录用的标签页')
            print('请保留爬虫用的标签页, 后续爬虫将自动执行')
            return True
    print('登陆等待超时，自动结束')
    return False

def get_user_id(driver):
    driver.get('https://www.zhihu.com')
    button_xpath = '(//button[@id="Popover15-toggle"])'
    wait_until(driver, button_xpath, timeout=10)
    ele = driver.find_element(By.XPATH, button_xpath)
    ele.click()
    user_id_xpath = '(//a[@class="Menu-item AppHeaderProfileMenu-item css-1e76yen"][@href])[1]'
    wait_until(driver, user_id_xpath, timeout=10)
    user_url = driver.find_element(By.XPATH, user_id_xpath)
    user_url = user_url.get_attribute('href')
    user_id = user_url.split('/')[-1]
    return user_id

def get_list(driver, user_id, category):
    driver.get(f'https://www.zhihu.com/people/{user_id}/{category}')
    wait_until(driver, '(//button[@class="Button PaginationButton PaginationButton--current Button--plain"])', timeout=10)
    page_ids = driver.find_elements(By.XPATH,'(//button[@class="Button PaginationButton PaginationButton--current Button--plain"])')
    page_ids += driver.find_elements(By.XPATH,'(//button[@class="Button PaginationButton Button--plain"])')
    page_num=max([int(page_id.text) for page_id in page_ids])

    # get titles, urls list
    titles, urls = [], []
    for page_id in range(1,page_num+1):
        driver.get(f'https://www.zhihu.com/people/{user_id}/{category}?page={page_id}')

        wait_success = wait_until(driver, '(//div[@class="PlaceHolder List-item"])', timeout=20, until_not=True)

        if category == 'pins':
            item_urls = driver.find_elements(By.XPATH,'(//div[@class="ContentItem-time"]//a[@href])')
            item_titles = ['' for i in item_urls]
        elif category in ['answers', 'posts', 'asks']:
            item_titles = driver.find_elements(By.XPATH,'(//h2[@class="ContentItem-title"]//a)')
            item_urls = driver.find_elements(By.XPATH,'(//h2[@class="ContentItem-title"]//a[@href])')

        for ind,i in enumerate(item_urls):
            if category == 'pins':
                title = ''
            elif category in ['answers', 'posts', 'asks']:
                title = item_titles[ind].text
            url = item_urls[ind].get_attribute('href')
            if url.startswith('/question'):
                url = 'https://www.zhihu.com'+url

            titles.append(title)
            urls.append(url)

        print(f'page {page_id} / {page_num}, titles {len(item_titles)} / {len(titles)}, urls {len(item_urls)} / {len(urls)}' \
             + ( '' if wait_success else '  Timeout'))

    for article_id, (title, url) in enumerate(zip(titles, urls)):
        print(article_id+1, title, url)

    return titles, urls

def save_pages(driver, save_dir, category, titles, urls):
    # save pages
    category_dir = f'{save_dir}/{category}'
    os.makedirs(category_dir, exist_ok=True) # if no such path exists, iteratively created the dir

    for article_id, (title, url) in enumerate(zip(titles, urls)):
        print(f'{article_id+1} / {len(titles)}', title, url)

        article_id = url.split('/')[-1]
        driver.get(url)

        if '你似乎来到了没有知识存在的荒原' in driver.title:
            print(title, url, '你似乎来到了没有知识存在的荒原')
            continue

        if category == 'posts':
            article_content = driver.find_element(By.XPATH,'(//div[@class="Post-RichTextContainer"])')
            article_time = driver.find_element(By.XPATH,'(//div[@class="ContentItem-time"])')
            article_time = article_time.text
        elif category == 'answers':
            article_content = driver.find_element(By.XPATH,'(//div[@class="RichContent-inner"])')
            article_time = driver.find_element(By.XPATH,'(//div[@class="ContentItem-time"]//span[@data-tooltip])')
            public_time = article_time.get_attribute('data-tooltip')
            edit_time = article_time.text
            article_time = public_time + ('&nbsp;' * 4) + edit_time
        elif category == 'pins':
            article_content = driver.find_element(By.XPATH,'(//div[@class="RichContent"])')
            # (//div[@class="RichText ztext PinItem-remainContentRichText"])
            # (//div[@class="ContentItem-time"])
        elif category == 'asks':
            button_xpath = '(//button[@class="Button QuestionRichText-more Button--plain"])'
            button_exits = wait_until(driver, button_xpath, timeout=5)
            if button_exits:
                elem = driver.find_element(By.XPATH,button_xpath)
                elem.click()

            content_xpath = '(//div[@class="QuestionRichText QuestionRichText--expandable"])'
            content_exits = wait_until(driver, content_xpath, timeout=5)
            if content_exits:
                article_content = driver.find_element(By.XPATH, content_xpath)
            else:
                article_content = ''

        if article_content != '':
            article_content = article_content.get_attribute('innerHTML')
        if category in ['answers', 'posts', 'asks']:
            article_content = f'<h1>{title}</h1><a href="{url}">原文链接</a>' + article_content
        if category in ['answers', 'posts']:
            article_time =  '<p>'+article_time+'</p>'
            article_content += article_time
        html = etree.HTML(article_content)


        video_elems = html.xpath('//div[@class="RichText-video"]')
        if video_elems != []:
            res = requests.get(url, headers=headers)
            # 获取答案url上的id
            if category[-1] == 's':
                category_remove_s = category[0:-1]
            answer_id = re.findall(category_remove_s+r'/(\d+)', url)[0]

            # 获取json文本
            text = res.text
            json_text = re.findall(r'<script id="js-initialData" type="text/json">(.*?)</script>', text)[0]

            # 提取答案的content文件。
            data = json.loads(json_text)
            content = data['initialState']['entities'][category][answer_id]['content']
            # 提取url
            if category == 'answers':
                video_urls = re.findall(r'(https://www.zhihu.com/video/\d+)', content)
                video_ids = [re.findall(r'/video/(\d+)', url)[0] for url in video_urls]
            elif category == 'pins':
                content = str(content)
                video_ids = re.findall(r"'videoId': '(\d+)'", content)


            video_codes = []
            for video_id in video_ids:
                video_url = f'https://lens.zhihu.com/api/v4/videos/{video_id}'
                res = requests.get(video_url, headers=headers)
                data = json.loads(res.text)

                if "HD" in data["playlist"].keys():
                    video_url = data["playlist"]["HD"]["play_url"]
                elif "SD" in data["playlist"].keys():
                    video_url = data["playlist"]["SD"]["play_url"]
                elif "LD" in data["playlist"].keys():
                    video_url = data["playlist"]["LD"]["play_url"]
                # LD（标清）, SD（高清）, HD（超清）
                video_name = data["title"]
                if video_name == None:
                    video_name = '视频'
                else:
                    video_name += '.mp4'

                video_url = video_url.replace('&', '&amp;')
                # video_html = f'''<iframe src="{video_url}" allowfullscreen="allowfullscreen" width="100%" height="600" scrolling="no" frameborder="0" sandbox="allow-top-navigation allow-same-origin allow-forms allow-scripts"></iframe>'''
                video_html = f'<p>{video_url}</p>'
                # video_codes.append(f'<a href="xxx">yyyy</a>')
                video_codes.append(video_html)

            for elem, code in zip(video_elems, video_codes):
                new_elem = etree.fromstring(code)
                elem.getparent().replace(elem, new_elem)

        # print('VideoCard-video', driver.find_element(By.XPATH, '(//div[@class="VideoCard-video"])'), '\n')
        # print('VideoCard-video-content', driver.find_element(By.XPATH, '(//div[@class="VideoCard-video-content"])'), '\n')
        # print('VideoCard-player', elem := driver.find_element(By.XPATH, '(//div[@class="VideoCard-player"])'), '\n')
        # elem.click()
        # print('iframe video', elem := driver.find_element(By.XPATH, '(//iframe[@title="video"])'), '\n')
        # elem.click()

        # driver.switch_to.frame(elem)
        # print('inside')
        # video_xpath = '(//video[@playsinline])'
        # if wait_until(driver, video_xpath, timeout=5):
        #     print('playsinline get')
        # else:
        #     print('waiting get nothing')
        # print()
        # print(driver.page_source)
        # driver.switch_to.default_content()

        article_content = etree.tostring(html, encoding='unicode', pretty_print=True)

        title = title.replace('/','\\')
        if category == 'pins':
            filename = article_id
        else:
            filename = f"{title}-{article_id}"
        with open(f"{category_dir}/{filename}.html", "w", encoding="utf-8") as f:
            f.write(article_content)


def main(save_dir, driver_path):
    driver = start_driver(driver_path)

    if login_zhihu(driver):
        user_id = get_user_id(driver)
        print('user_id =', user_id)
        print('\n################### Started ###################')

        categories = [ 'posts', 'answers', 'pins', 'asks' ]  #  'collections', 'columns'
        for category in categories:
            print(f'\n=================== {category} ===================')
            print(f'---------------- Collecting Pages ----------------')
            titles, urls = get_list(driver, user_id, category)
            print(f'------------------ Saving Pages ------------------')
            save_pages(driver, save_dir, category, titles, urls)

        print('\n################### Finished ###################')

    driver.close()
    driver.quit()

if __name__ == "__main__":
    normal_chrome = NormalChrome(chrome_log)
    try:
        main(save_dir, driver_path)
    finally:
        normal_chrome.close()
