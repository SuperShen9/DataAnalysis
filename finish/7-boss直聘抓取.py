# -*- coding: utf-8 -*-
# author：Super

import pandas as pd
from build.Func import or_path

import requests
import time
from lxml import etree
from pyquery import PyQuery

headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    'cookie': "JSESSIONID=""; __c=1530137184; sid=sem_pz_bdpc_dasou_title; __g=sem_pz_bdpc_dasou_title; __l=r=https%3A%2F%2Fwww.zhipin.com%2Fgongsi%2F5189f3fadb73e42f1HN40t8~.html&l=%2Fwww.zhipin.com%2Fgongsir%2F5189f3fadb73e42f1HN40t8~.html%3Fka%3Dcompany-jobs&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1531150234,1531231870,1531573701,1531741316; lastCity=101010100; toUrl=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3Dpython%26scity%3D101010100; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1531743361; __a=26651524.1530136298.1530136298.1530137184.286.2.285.199",
    'origin': "https://www.zhipin.com",
    'referer': "https://www.zhipin.com/job_detail/?query=python&scity=101010100",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

url_b = 'https://www.zhipin.com/'


def init():
    df_all = pd.DataFrame()
    for count in range(1, 10):
        url = 'https://www.zhipin.com/c101210100/?query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88&page={}'.format(
            count)

        if count == 1:
            div = 3
        else:
            div = 2

        html = requests.get(url, headers=headers).text

        tree = etree.HTML(html)

        res = PyQuery(html)

        df = pd.DataFrame()
        for i in range(30):
            df.loc[i, '公司'] = res(
                'li:nth-child({}) > div > div.info-company > div > h3 > a'.format(i + 1)).text()

            df.loc[i, '职位'] = res(
                'li:nth-child({}) > div > div.info-primary > h3 > a > div.job-title'.format(i + 1)).text()

            df.loc[i, '薪水'] = res(
                'li:nth-child({}) > div > div.info-primary > h3 > a > span'.format(i + 1)).text()

            df.loc[i, '地区'] = \
                tree.xpath('//*[@id="main"]/div/div[{}]/ul/li[{}]/div/div[1]/p/text()[1]'.format(div, i + 1))[0]

            df.loc[i, '经验要求'] = \
                tree.xpath('//*[@id="main"]/div/div[{}]/ul/li[{}]/div/div[1]/p/text()[2]'.format(div, i + 1))[0]

            df.loc[i, '学历要求'] = \
                tree.xpath('//*[@id="main"]/div/div[{}]/ul/li[{}]/div/div[1]/p/text()[3]'.format(div, i + 1))[0]

            df.loc[i, '行业'] = \
                tree.xpath('//*[@id="main"]/div/div[{}]/ul/li[{}]/div/div[2]/div/p/text()[1]'.format(div, i + 1))[0]

            df.loc[i, '融资'] = \
                tree.xpath('//*[@id="main"]/div/div[{}]/ul/li[{}]/div/div[2]/div/p/text()[2]'.format(div, i + 1))[0]
            try:
                df.loc[i, '人数'] = \
                    tree.xpath('//*[@id="main"]/div/div[{}]/ul/li[{}]/div/div[2]/div/p/text()[3]'.format(div, i + 1))[0]
            except IndexError:
                print('\n{} - 该公司有数据缺失！\n'.format(df.loc[i, '公司']))

            df.loc[i, 'url'] = url_b + res('li:nth-child({}) > div > div.info-primary > h3 > a'.format(i + 1)).attr.href

        time.sleep(5)

        df_all = df_all.append(df, ignore_index=True)
        print('第{}页抓取完毕！……'.format(count))

    df_all.to_excel(or_path('boss直聘数据分析岗位'))


import os

file = 'C:\\Users\Administrator\Desktop\\boss直聘数据分析岗位.xlsx'
if os.path.exists(file):
    print('\n{} - 已存在！\n'.format('岗位数据已存在'))
else:
    init()

df = pd.read_excel(or_path('boss直聘数据分析岗位'))

df.drop_duplicates('url', inplace=True)


def content():
    df2 = pd.DataFrame()
    for i in range(df.shape[0]):
        html2 = requests.get(df.loc[i, 'url'], headers=headers).text
        tree2 = etree.HTML(html2)

        df2.loc[i, 'url'] = df.loc[i, 'url']


        df2.loc[i, 'HR状态'] = tree2.xpath('//*[@id="main"]/div[3]/div/div[2]/div[1]/p/text()')[1]

        df2.loc[i, '工作内容'] = str(tree2.xpath('//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div/text()'))
        df2.loc[i, '公司介绍'] = str(tree2.xpath('//*[@id="main"]/div[3]/div/div[2]/div[2]/div[2]/div/text()[2]'))

        df2.loc[i, '法人代表'] = tree2.xpath('//*[@class="level-list"]//text()')[2]
        df2.loc[i, '注册资金'] = tree2.xpath('//*[@class="level-list"]//text()')[5]
        df2.loc[i, '成立时间'] = tree2.xpath('//*[@class="level-list"]//text()')[8]

        print(df2.loc[i, '法人代表'])

        print('第{}页抓取完毕！……'.format(i + 1))

        time.sleep(3)

    return df2


# df2 = content()
# df = pd.merge(df, df2, on='url', how='left')
#
# df.to_excel(or_path('boss直聘数据分析岗位content'))

if __name__ == "__main__":
    pass
