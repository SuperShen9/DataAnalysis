# -*- coding: utf-8 -*-
# author：Super.Shen

import networkx as nx

# 有向图之间边的关系
edges = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "A"), ("B", "D"), ("C", "A"), ("D", "B"), ("D", "C")]

# 创建有向图
graph = nx.DiGraph()

# print(type(graph))
# print(graph)
# exit()


# 添加节点
for x in edges:
    graph.add_edge(x[0], x[1])

print('\n节点个数：', graph.number_of_nodes())
print('\n各个节点：', graph.nodes())

# print(graph.edges())

# 计算权重值
pagerank = nx.pagerank(graph, alpha=1)
print("\npagerank 值是：", pagerank)



