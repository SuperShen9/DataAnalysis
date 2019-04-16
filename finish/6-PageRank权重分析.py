# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict


# 画网络图
def show_graph(graph, layout=3):
    # 在圆上定位节点
    if layout == 1:
        positions = nx.circular_layout(graph)

    # 均匀随机定位节点
    elif layout == 2:
        positions = nx.random_layout(graph)

    # 将节点定位在同心圆中
    elif layout == 3:
        positions = nx.shell_layout(graph)

    # 使用 Spring Layout 布局，类似中心放射状
    elif layout == 4:
        positions = nx.spring_layout(graph)

    # 特征向量定位节点
    else:
        positions = nx.spectral_layout(graph)

    # 设置网络图中的节点大小，因为 pagerank 值很小所以需要 *10000
    nodesize = [x['pagerank'] * 10000 for v, x in graph.nodes(data=True)]

    # 设置网络图中的边长度
    edgesize = [(e[2]['weight']) for e in graph.edges(data=True)]

    # 绘制节点
    nx.draw_networkx_nodes(graph, positions, node_size=nodesize, alpha=0.4)

    # 绘制边
    nx.draw_networkx_edges(graph, positions, edge_size=edgesize, alpha=0.3)

    # 绘制节点的 label
    nx.draw_networkx_labels(graph, positions, font_size=10)

    # 输出关系图
    plt.show()


# 读取数据
df = pd.read_excel('E:\BaiduYunDownload\weixin\PageRank\data.xlsx')

list1 = []
list2 = []

# 用字典的方式读取dataframe
for x, y in df.iterrows():
    list1.append((str(y[0]), str(y[1])))
    list2.append(y[2])


# 有向图之间边的关系
edges = list1

# 创建有向图
graph = nx.DiGraph()

# 生成防错字典
edges_weights_temp = defaultdict(list)

# 填充有向数据和边长参数
count = 0
for edge in edges:
    graph.add_edge(edge[0], edge[1])

    temp = (edge[0], edge[1])
    if temp not in edges_weights_temp:
        edges_weights_temp[temp] = list2[count]
    else:
        edges_weights_temp[temp] = edges_weights_temp[temp] + list2[count]
    count += 1

    # # 加判断看一下效果
    # if count <= 4:
    #     print(edges_weights_temp)
    # else:
    #     exit()

# 把防错字典转化为列表
edges_weights = [(key[0], key[1], val) for key, val in edges_weights_temp.items()]

# 设置有向图的路径及权重
graph.add_weighted_edges_from(edges_weights)

# 计算PR值
pagerank = nx.pagerank(graph)
# print("\npagerank 值是：", pagerank)

# 将PR值作为节点属性
nx.set_node_attributes(graph, name='pagerank', values=pagerank)

# 展示网格图
show_graph(graph)


# --------------剔除权重低的节点-----------------------------

# 筛选大于阈值的重要核心节点
pagerank_threshold = 0.02

# 复制一份计算好的网络图
small_graph = graph.copy()

# 剪掉PR值小于pagerank_threshold的节点
for n, p_rank in graph.nodes(data=True):
    if p_rank['pagerank'] < pagerank_threshold:
        small_graph.remove_node(n)

# 画网络图,随机踩点
show_graph(small_graph, 2)
