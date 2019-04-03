# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import datetime
import os
import shutil

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
bef_yesterday = today - datetime.timedelta(days=2)
hour = datetime.datetime.now().strftime('%H')

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')


def or_path(file_name):
    return 'C:\\Users\Administrator\Desktop\\{}.xlsx'.format(file_name)


# 读取xlsx文件的时候用sheet写入
def du_excel(sheet_name):
    try:
        # 读取数据
        df = pd.read_excel('C:\\Users\Administrator\Desktop\\A_奇奇乐每日数据\\奇奇乐.xlsx', sheet_name=sheet_name)
        return df
    except FileNotFoundError:
        print('\n缺少运行数据，请先下载……')
        exit()


# 读取xls文件的时候还是使用excel名称写入
def du_old_excel(excel_name):
    try:
        # 读取数据
        df = pd.read_excel('C:\\Users\Administrator\Desktop\\A_奇奇乐每日数据\\{}.xls'.format(excel_name))
        return df
    except FileNotFoundError:
        print('\n缺少运行数据，请先下载……')
        exit()


# 优化groupby之后的输出结果
def gb(df, gb_col, sum_col):
    df_m = df.groupby(gb_col)[sum_col].sum()
    df_m = pd.DataFrame(df_m)
    df_m.reset_index(inplace=True)
    df_m.sort_values(sum_col, ascending=0, inplace=True)
    df_m.reset_index(drop=True, inplace=True)
    return df_m


# 切割函数
def df_cut(df, gb_col, sum_col):
    df_m = gb(df, gb_col, sum_col)
    bins = [5, 100, 200, 500, 1000, 2000, 100000]
    df_c = pd.cut(df_m[sum_col], bins, right=False)
    df_c = pd.DataFrame(df_c)
    df_c = df_c.groupby(sum_col).size()
    return df_c


# 求和功能
def df_sum(df):
    i = 10000
    df.loc[i, '用户id'] = '汇总：'
    df.loc[i, '昵称'] = '{}人'.format(df.shape[0] - 1)
    df.loc[i, '充值金额'] = df['充值金额'].sum()
    df.loc[i, '兑换金额'] = df['兑换金额'].sum()
    df.loc[i, '单用户盈利'] = df['单用户盈利'].sum()
    df.loc[i, '累计红宝石产出'] = df['累计红宝石产出'].sum()
    df = df.reset_index(drop=True)

    return df


'-----------------------------时间排序------------------------------------------'


def time_sort(df, col):
    df[col] = df[col].apply(lambda x: pd.to_datetime(x))
    df.sort_values(col, inplace=True)
    return df


# ----------------------------剪贴文件------------------------------------------------------
def cut_file(name, yue, ri):
    or_path = 'C:\\Users\Administrator\Desktop\\'
    tar_path = 'C:\\Users\Administrator\Desktop\\{}-{}-{}\\'.format(name, yue, ri)

    if name == '奇奇乐':
        list1 = ['run_奇奇乐', '奇奇乐平均数据', '奇奇乐推广费', '奇奇乐总表']
    elif name == '浪仔':
        list1 = ['run_浪仔', '浪仔平均数据', '浪仔推广费', '浪仔总表']
        # '浪仔截止','奇奇乐截止',

    elif name == '每日CPA数据':
        list1 = ['CPA数据', 'CPA留存', '浪仔CPA渠道截止昨日数据概况']
    else:
        print('cut_file 功能：请输入正确平台名称。')
        exit()

    for i in os.listdir(or_path):
        for y in list1:
            if i.startswith(y):
                shutil.move(or_path + i, tar_path + i)


# 炮口用户体验里的-复制
def cut_file_JN(name, yue, ri):
    or_path = 'C:\\Users\Administrator\Desktop\\'
    tar_path = 'C:\\Users\Administrator\Desktop\\{}-{}-{}\\'.format(name, yue, ri)

    if name == '奇奇乐':
        list1 = ['奇奇乐截止', ]
    elif name == '浪仔':
        list1 = ['浪仔截止', ]

    elif name == '每日CPA数据':
        list1 = ['CPA数据', 'CPA留存', '浪仔CPA渠道截止昨日数据概况']
    else:
        print('cut_file 功能：请输入正确平台名称。')
        exit()

    for i in os.listdir(or_path):
        for y in list1:
            if i.startswith(y):
                shutil.move(or_path + i, tar_path + i)


# ---------------------------------------------------------------------------------------------

def hbc_cal(df):
    # 数据分析
    df['变动时间'] = df['变动时间'].apply(lambda x: pd.to_datetime(x))

    df.sort_values('变动时间', inplace=True)

    df = pd.DataFrame(df.groupby(['用户ID', '变动属性'])['差值'].sum())
    df.reset_index(inplace=True)

    df = pd.pivot_table(df, values='差值', index='用户ID', columns='变动属性')
    df.reset_index(inplace=True)

    try:
        df = df[['用户ID', '金币', '红宝石']]
    except KeyError:
        df = df[['用户ID', '金币', '红包券']]

    df.fillna(0, inplace=True)

    df['金币赢取'] = df['金币'] / 17000

    try:
        df['宝石赚取'] = df['红宝石'] / 10
        df.sort_values('红宝石', inplace=True, ascending=0)
    except KeyError:
        df['宝石赚取'] = df['红包券'] / 10
        df.sort_values('红包券', inplace=True, ascending=0)

    df['求和'] = df['金币赢取'] + df['宝石赚取']

    df.reset_index(drop=True, inplace=True)

    return df


# --------------------------将Excel文件写入txt------------------------------------------

def to_txt(target_file, to_file, sp):
    df = pd.read_excel(or_path(target_file))

    def write(col):
        path = 'C:\\Users\Administrator\Desktop\\'
        fl = open(path + '{}.txt'.format(to_file), 'w')
        for x in range(df.shape[0]):
            fl.write(str(df.loc[x, col]))
            if x < df.shape[0] - 1:
                fl.write(sp)

        fl.close()

    if '数据' not in df.columns:
        print('\n默认取表格第一列数值.')
        col = df.columns[0]
        write(col)
    else:
        print('\n读取[数据]列，并进行合并.')
        write('数据')

