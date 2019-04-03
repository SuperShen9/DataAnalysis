# -*- coding: utf-8 -*-
# author：Super.Shen


url = 'https://www.zhipin.com/c101020100/h_101020100/?query=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&page='

url2 =   'https://www.zhipin.com/c101210100/?query=Python&page=2&ka=page-'
headers = {
    'user-agent': 'Mozilla/5.0'
}
page = 1
hud = ['职位名', '薪资1', '薪资2', '职位名', '地点', '经验', '学历', '公司行业', '融资阶段', '公司人数', '发布日期', '发布人']
print('\t'.join(hud))

import requests
from bs4 import BeautifulSoup
import time

for n in range(1, 11):
    html = requests.get(url2 + str(page), headers=headers)

    page += 1
    soup = BeautifulSoup(html.text, 'html.parser')
    for item in soup.find_all('div', 'job-primary'):
        shuchu = []
        shuchu.append(item.find('div', 'job-title').string)  # 职位名

        xinzi = item.find('span', 'red').string
        xinzi = xinzi.replace('k', '')
        xinzi = xinzi.split('-')
        shuchu.append(xinzi[0])  # 薪资起始数
        shuchu.append(xinzi[1])  # 薪资起始数

        yaoqiu = item.find('p').contents
        shuchu.append(yaoqiu[0].string if len(yaoqiu) > 0 else 'None')  # 地点
        shuchu.append(yaoqiu[2].string if len(yaoqiu) > 2 else 'None')  # 经验
        shuchu.append(yaoqiu[4].string if len(yaoqiu) > 4 else 'None')  # 学历

        gongsi = item.find('div', 'info-company').find('p').contents
        shuchu.append(gongsi[0].string if len(gongsi) > 0 else 'None')  # 公司行业
        shuchu.append(gongsi[2].string if len(gongsi) > 2 else 'None')  # 融资阶段
        shuchu.append(gongsi[4].string if len(gongsi) > 4 else 'None')  # 公司人数

        shuchu.append(item.find('div', 'info-publis').find('p').string.replace('发布于', ''))  # 发布日期
        shuchu.append(item.find('div', 'info-publis').find('h3').contents[3].string)  # 发布人

        print('\t'.join(shuchu))
        time.sleep(1)