import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

os.chdir('D:\jupyter\Project\Demo_L3')


def get_html(url):
    try:
        response = requests.get(url)
        return response
    except Exception as e:
        print(e)
        return None


# 获得地区url地址
def find_cat_url(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, "lxml")
    soup_set = soup.find('div', attrs={'class': 'hot-list clearfix'}).find_all('dt')  # 查找热门目的地直辖市或省
    cat_url = []
    cat_name = []
    for i in range(0, len(soup_set)):
        for j in range(0, len(soup_set[i].find_all('a'))):
            cat_url.append(soup_set[i].find_all('a')[j].attrs['href'])  # 获取每个地区的本地超链接
            cat_name.append(soup_set[i].find_all('a')[j].text)  # 获取地区名字
    cat_url = ['http://www.mafengwo.cn' + cat_url[i] for i in range(0, len(cat_url))]  # 生成每个地区的URL
    return cat_url


# 获得城市名词和id
def find_city_url(url_list):  # 参数为每个地区url
    city_name_list = []
    city_url_list = []
    for i in range(0, len(url_list)):
        driver = webdriver.Chrome()
        driver.maximize_window()
        url = url_list[i].replace('travel-scenic-spot/mafengwo', 'mdd/citylist')  # 修改URL为该地区热门城市URL
        driver.get(url)  # 浏览器打开某地区热门城市页面
        while True:
            # 在某地区热门城市页面查找每一个目的地
            try:
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                url_set = soup.find_all('a', attrs={'data-type': '目的地'})
                # 获取城市中文名
                city_name_list = city_name_list + [url_set[i].text.replace('\n', '').split()[0] for i in
                                                   range(0, len(url_set))]
                # 获取目的地id
                city_url_list = city_url_list + [url_set[i].attrs['data-id'] for i in range(0, len(url_set))]
                js = "var q=document.documentElement.scrollTop=800"  # 获取浏览器滚动条
                driver.execute_script(js)
                time.sleep(2)
                driver.find_element_by_class_name('pg-next').click()  # 下一页
            except:
                break  # 最后一页爬取完后结束循环
        driver.close()
    return city_name_list, city_url_list


# 获取所有目的地和对应id
def city_url_all():
    url = 'http://www.mafengwo.cn/mdd/'
    url_list = find_cat_url(url)
    city_name_list, city_url_list = find_city_url(url_list)
    city = pd.DataFrame({'city': city_name_list, 'id': city_url_list})


city_url_all()
