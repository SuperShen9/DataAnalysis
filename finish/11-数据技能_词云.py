# -*- coding: utf-8 -*-
# author：Super.Shen

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import jieba
import pandas as pd
from build.Func import or_path
import re

# 查找单词
pattern = re.compile(r'[A-Za-z]+')

# 读取数据
def read_data(type=1):
    df = pd.read_excel(or_path('boss直聘数据分析岗位content'))
    words = ''
    for i in range(df.shape[0]):
        content = str(df.loc[i, '工作内容'])

        # 读取中文
        if type == 1:
            words = " ".join(jieba.cut(content))

        # 读取英文
        else:
            content = pattern.findall(content)
            for n in content:
                if n == 'R':
                    words = words + ' ' + n
                elif (len(n) > 1):
                    words = words + ' ' + n

    return words

type = 1
text = read_data(type)

# 生成词云
def create_word_cloud(text):
    stopwords = set(STOPWORDS)
    stopwords.add("数据")
    stopwords.add("分析")
    stopwords.add("岗位职责")
    stopwords.add("xa")

    wc = WordCloud(
        font_path="C:\Windows\Fonts\SimHei.ttf",
        max_words=100,
        width=2000,
        height=1200,
        stopwords=stopwords
    )

    # 生成数据
    wordcloud = wc.generate(text)

    # 写词云图片
    wordcloud.to_file("C:\\Users\Administrator\Desktop\wordcloud{}.jpg".format(type))

    # 显示词云文件
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

create_word_cloud(text)
