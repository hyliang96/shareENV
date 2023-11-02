import re
from lxml import etree

fname = '../zhihu_backup/posts/两个决不会被严重曲解了，不能用它为延续资本主义辩护-450904830.html'

def print_node(node):
    print(etree.tostring(node, pretty_print=True, encoding='unicode'))

def url_dezhihu(url):
    url = url.replace('https://link.zhihu.com/?target=', '')
    url = url.replace('%3A//', '://')
    return url

with open(fname, 'r') as f:
    text = f.read()

    title = re.search(r'<h1>(.+?)</h1>', text).group(1)
    url = re.search(r'<a href="(.+?)">原文链接</a>', text).group(1)
    time = re.findall(r'<div>编辑于 (.+?)</div>', text)[-1]

    parser = etree.XMLParser(remove_blank_text=True)
    content = etree.fromstring(text, parser=parser)
    content = content.xpath('//div[starts-with(@class, "RichText ztext Post-RichText")]')[0]

    content_list = content.xpath('//h2')
    for c in content_list:
        text = c.text
        text = f'<p>## {text}</p>'
        new_c = etree.XML(text)
        c.getparent().replace(c, new_c)

    content_list = content.xpath('//h3')
    for c in content_list:
        text = c.text
        text = f'<p>### {text}</p>'
        new_c = etree.XML(text)
        c.getparent().replace(c, new_c)

    content_list = content.xpath('//h4')
    for c in content_list:
        text = c.text
        text = f'<p>#### {text}</p>'
        new_c = etree.XML(text)
        c.getparent().replace(c, new_c)

    content_list = content.xpath('//h5')
    for c in content_list:
        text = c.text
        text = f'<p>##### {text}</p>'
        new_c = etree.XML(text)
        c.getparent().replace(c, new_c)

    content_list = content.xpath('//h6')
    for c in content_list:
        text = c.text
        text = f'<p>###### {text}</p>'
        new_c = etree.XML(text)
        c.getparent().replace(c, new_c)

    content_list = content.xpath('//blockquote')
    for c in content_list:
        print(c.attrib['data-pid'], c.text)
        text = c.text
        text = f'<p>&gt; {text}</p>'
        new_c = etree.XML(text)
        c.getparent().replace(c, new_c)

    content_list = content.xpath('//a[@class=" external" or @class="internal"]')
    for c in content_list:
        url = url_dezhihu(c.attrib['href'])
        tag_url = f'<a>&lt;{url}&gt;</a>'
        new_c = etree.XML(tag_url)
        c.getparent().replace(c, new_c)

    content_list = content.xpath('//div[@class="RichText-LinkCardContainer"]')
    for c in content_list:
        c_ = etree.fromstring(etree.tostring(c), parser=parser)
        img_node = c_.xpath('//a[@href]')[0]
        url = url_dezhihu(img_node.attrib['href'])
        tag = img_node.attrib['data-text']
        tag_url = f'[{tag}]({url})'
        new_c = etree.XML(f'<p>{tag_url}</p>')
        c.getparent().replace(c, new_c)

    content_list = content.xpath('//figure')
    for c in content_list:
        c_ = etree.fromstring(etree.tostring(c), parser=parser)
        url = url_dezhihu(c_.xpath('//img[@src]')[0].attrib['src'])
        tag_url = f'![]({url})'
        new_c = etree.XML(f'<p>{tag_url}</p>')
        c.getparent().replace(c, new_c)

    # text = etree.HTML(text)
    content = etree.tostring(content, encoding='unicode')

    content = re.sub(r'\<div class="RichText ztext Post-RichText[^\>]*?\>', '', content)
    content = re.sub(r'\</div\>', '', content)
    content = re.sub(r'\<p[^\>]*?\>', '\n', content)
    content = re.sub(r'\</p\>', '\n', content)
    # content = content.replace('<br/>', '\n\n')
    content = content.replace('<b>', '**')
    content = content.replace('</b>', '**')
    content = content.replace('<a>', '')
    content = content.replace('</a>', '')
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')


    content = \
        f'{title}\n\n'+ \
        f'<{url}>\n\n'+ \
        f'编辑于: {time}\n\n' + \
        content

    # print(content)



    # content = re.search(r'<div class=".+?">([\s\S]+)</div>', text).group(1)

    # <p data-pid="AcipohW1">其实， “摸着石头过河”来源于四川民间鬼怪故事：</p>





# https://3yya.com/lesson/66

# https://www.gairuo.com/p/python-selenium

# https://itsmycode.com/executable-path-has-been-deprecated/

# https://blog.csdn.net/Rebacca122222/article/details/123843492

# https://blog.csdn.net/weixin_47163937/article/details/115330332


# html = etree.HTML(driver.page_source)
# print(title, url)
# print('html =', html)
# print('html.txt =', etree.tostring(html, pretty_print=True).decode('utf-8'))
# txt = '\n'.join(map(lambda x:etree.tostring(x), html.xpath('(//div[@class="Post-RichTextContainer"])')))

# //*[@id="root"]/div/main/div/article/div[1]
# (//div[@class="Post-RichTextContainer"])
# (//div[@class="RichContent-inner"])


# elem = driver.find_element(By.LINK_TEXT,'我的主页')
# elem.click()

# import requests
# s = requests.Session()
# selenium_user_agent = driver.execute_script("return navigator.userAgent;")
# s.headers.update({"user-agent": selenium_user_agent})
# for cookie in driver.get_cookies():
#     s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

# # 发起访问请求
# r = s.get(f'https://www.zhihu.com/people/{user_id}/{category}')
# print(r)

# plcaeholder = driver.find_elements(By.XPATH, '(//div[@class="PlaceHolder List-item"])')
# print('plcaeholder', plcaeholder)

# driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')



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
