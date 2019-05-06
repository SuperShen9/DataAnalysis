# -*- coding: utf-8 -*-
# author：Super

# 清洗模型
import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)

# 工具导入
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# 算法模型导入
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

# 剔除警告
import warnings

warnings.filterwarnings('ignore')

# 读取数据
df = pd.read_csv('E:\BaiduYunDownload\weixin\credit\data.csv')

# # 数据探索
# print(df.shape)
# print(df.describe())

# 删除无效列
df.drop('ID', axis=1, inplace=True)

# 选取特征
features = df[df.columns[:-1]]
target = df[df.columns[-1:]]

# 30% 作为测试集，其余作为训练集
train_x, test_x, train_y, test_y = train_test_split(features,
                                                    target, test_size=0.30, stratify=target, random_state=1)


# 构造各种分类器
classifiers = [
    AdaBoostClassifier(random_state=1),
    SVC(random_state=1, kernel='rbf'),
    DecisionTreeClassifier(random_state=1, criterion='gini'),
    RandomForestClassifier(random_state=1, criterion='gini'),
    KNeighborsClassifier(metric='minkowski'),
]

# 分类器名称
classifier_names = [
    'adaBoostClassifier',
    'svc',
    'decisiontreeclassifier',
    'randomforestclassifier',
    'kneighborsclassifier',
]

# 分类器参数
classifier_param_grid = [
    {'adaBoostClassifier__n_estimators': range(30, 80, 10)},
    {'svc__C': [1], 'svc__gamma': [0.01]},
    {'decisiontreeclassifier__max_depth': [6, 9, 11]},
    {'randomforestclassifier__n_estimators': [3, 5, 7]},
    {'kneighborsclassifier__n_neighbors': [4, 6, 8]},
]


# 对具体的分类器进行 GridSearchCV 参数调优
def GridSearchCV_work(pipeline, param_grid, score='accuracy'):
    response = pd.DataFrame()
    gridsearch = GridSearchCV(estimator=pipeline, param_grid=param_grid, scoring=score)

    # 寻找最优的参数 和最优的准确率分数
    search = gridsearch.fit(train_x, train_y)
    print("GridSearch 最优参数：", search.best_params_)
    print("GridSearch 最优分数： %0.4lf" % search.best_score_)

    # 输出拟合结果
    predict_y = gridsearch.predict(test_x)
    print("#准确率： %0.4lf" % accuracy_score(test_y, predict_y))
    response['predict_y'] = predict_y
    return response


from build.Func import or_path

df_all = pd.DataFrame()
for model, model_name, model_param_grid in zip(classifiers, classifier_names, classifier_param_grid):
    # print(model_name, '\n', '-' * 50)
    # print(model_param_grid, '\n', '-' * 50)
    # print(model)

    # 管道流水机制
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        (model_name, model)
    ])

    print('\n{}模型输出结果：'.format(model_name))

    # 参数调优
    result = GridSearchCV_work(pipeline, model_param_grid, score='accuracy')

    result.columns = [model_name]

    df_all = pd.concat([df_all, result], axis=1)

    print('-' * 50)

df_all.to_excel(or_path('各算法预测结果'))



