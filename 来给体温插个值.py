#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-12-18 13:59
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : 来给体温插个值.py
# @Software: PyCharm

import re

import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
from matplotlib import font_manager

plt.style.use("seaborn-pastel")

# 字体加载
font_path = r"C:\Users\lenovo\AppData\Local\Microsoft\Windows\Fonts\Alibaba-PuHuiTi-Regular.ttf"
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)
print(prop.get_name())  # 显示当前使用字体的名称

# 字体设置
font_manager.rcParams['font.family'] = 'sans-serif'  # 使用字体中的无衬线体
font_manager.rcParams['font.sans-serif'] = prop.get_name()  # 根据名称设置字体
font_manager.rcParams['font.size'] = 20  # 设置字体大小
font_manager.rcParams['axes.unicode_minus'] = False  # 使坐标轴刻度标签正常显示正负号

file = open('./COVID-19 感染记录.md', mode='r', encoding='utf-8')
content = file.read()
data = re.findall(r'\| (\d\d\d\d-\d\d-\d\d \d\d:\d\d) \| (\d\d\.\d) \|', content)

data_df = pd.DataFrame(data, columns=['时间', '体温'])
data_df['时间'] = pd.to_datetime(data_df['时间'])
data_df['体温'] = data_df['体温'].astype(float)
data_df.index = data_df['时间']

x = pd.date_range(min(data_df['时间']), max(data_df['时间']), freq='min')
data_map = pd.DataFrame()
data_map.index = x
for index in data_map.index:
    if index in data_df['时间']:
        data_map.loc[index, '体温'] = data_df.loc[index, '体温']

data_map['index'] = range(data_map.shape[0])
x = data_map[data_map.notnull()['体温']]['index'].to_list()
y = data_map[data_map.notnull()['体温']]['体温'].to_list()

f = interpolate.interp1d(x, y, kind=2)
newy = f(data_map['index'].to_list())

plt.plot(data_map.index, newy)
plt.scatter(data_df['时间'], data_df['体温'], s=15, color='#FF9900')
plt.xticks(rotation=0, size=8)
yticks = range(33, 40)
plt.yticks(yticks, [str(i) + '℃' for i in yticks], size=12)
plt.savefig('pic.svg')
plt.show()
