from requests import options
from selenium import webdriver  # 用来驱动浏览器的
import time
import selenium
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import os
os.startfile("/Applications/Safari.app") # 打开设置好的浏览器快捷方式
options = Options() # 得到edge的设置
options.add_experimental_option("debuggerAddress", "127.0.0.1:6001") # 配置浏览器的端口地址
#options.add_experimental_option('excudeSwitches',['enable-automation'])
driver=webdriver.Edge(service =Service("D:\\BaiduNetdiskWorkspace\\Lite Code\\python脚本\\firefox_selenium\\msedgedriver.exe"),options=options) # 浏览器驱动的放置地址
time.sleep(3)
write = ""

def get_all_folder(url):
    driver.get(url)
    time.sleep(2)
    href=[]
    title = driver.find_elements(By.XPATH,'(//a[@class="SelfCollectionItem-title"])')
    for ind,i in enumerate(title):
        href.append(title[ind].get_attribute('href'))
    return href

def pythonpazhihu(url,write):
    driver.get(url)
    time.sleep(3)
    #h2 = driver.find_elements(By.CLASS_NAME,"ContentItem-title")
    title = driver.find_elements(By.XPATH,'(//h2[@class="ContentItem-title"]//a)')
    h3 = driver.find_elements(By.XPATH,'(//h2[@class="ContentItem-title"]//a[@href])')
    for ind,i in enumerate(h3):
        content = str(title[ind].text)+" , "+str(h3[ind].get_attribute('href'))
        write=write+content+"\n"
        print(title[ind].text,h3[ind].get_attribute('href'))
    #print(h3.text)
    time.sleep(2)
    return write
try:
    url_all1 = "https://www.zhihu.com/collections/mine?page=1" # 总收藏也有两页，得到这两页每个收藏夹的具体链接
    url_all2 = "https://www.zhihu.com/collections/mine?page=2"
    href1 = get_all_folder(url_all1)
    href2 = get_all_folder(url_all2)
    href2 = href1+href2
    #print(href2)
    for url_son in href2:
        for i in range(5):
            #url = 'https://www.zhihu.com/collection/7179314xx?page=%s'%(i+1)
            url = url_son+'?page=%s'%(i+1) # 对每个收藏夹链接进行5页的循环
            write = pythonpazhihu(url,write) # 把读到的标题和链接写到write变量中
finally:
    driver.close()
    with open("./zhihu.txt","w",encoding="utf-8") as fp:
        fp.write(write)