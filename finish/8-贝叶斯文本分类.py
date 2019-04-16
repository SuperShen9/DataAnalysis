# -*- coding: utf-8 -*-
# author：Super

import os
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

# 目标路径
stop_path = 'E:\BaiduYunDownload\weixin\\文本分类\\stop\stopword.txt'
train_path = 'E:\BaiduYunDownload\weixin\\文本分类\\train\\'
test_path = 'E:\BaiduYunDownload\weixin\\文本分类\\test\\'

# 提取标签
def labels(path):
    list_l = []
    count = 0
    for x, y, z in os.walk(path):
        if count == 0:
            labels = y
        else:
            list_l.append(len(z))

        count += 1

    return labels, list_l


labels1, labels_len1 = labels(train_path)
labels2, labels_len2 = labels(test_path)

# 匹配标签
def fit_labels(labels, labels_len):
    fit_labels = []
    for x in range(len(labels)):
        fit_labels += list(labels[x].split(' ')) * labels_len[x]

    return fit_labels

train_labels = fit_labels(labels1, labels_len1)
test_labels = fit_labels(labels2, labels_len2)

# 提取数据
def get_data(path, labels):
    contents = []

    for label in labels:
        for x, y, z in os.walk(path + label):
            for file in z:
                word = open(x + '\\' + file, 'rb').read()
                words = " ".join(jieba.cut(word))
                contents.append(words)
    return contents


train_contents = get_data(train_path, labels1)
test_contents = get_data(test_path, labels2)

# 加载停用表
stop_words = [line.strip().decode('utf-8') for line in open(stop_path, 'rb').readlines()]
#
# 计算单词的权重
tf = TfidfVectorizer(stop_words=stop_words, max_df=0.5)
train_features = tf.fit_transform(train_contents)

# 多项式贝叶斯分类器
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB(alpha=0.001).fit(train_features, train_labels)

# 分类器做预测
test_tf = TfidfVectorizer(stop_words=stop_words, max_df=0.5, vocabulary=tf.vocabulary_)
test_features = test_tf.fit_transform(test_contents)
predicted_labels = clf.predict(test_features)

# 输出准确率
from sklearn import metrics

acc = metrics.accuracy_score(test_labels, predicted_labels)
print('贝叶斯模型预测准确率：', acc)
