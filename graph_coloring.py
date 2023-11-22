# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 17:52:30 2022

@author: litsas7
"""


import sys
import argparse
import collections
import math

program = sys.argv[1]
colours = int(sys.argv[2])
first = int(sys.argv[3])
graph = sys.argv[4]
g = {}

with open(graph) as graph_input:
    for line in graph_input:
        nodes = [int(x) for x in line.split()]
        if len(nodes) != 2:
            g[nodes[0]] = []
            continue
        if nodes[0] not in g:
            g[nodes[0]] = []
        if nodes[1] not in g:
            g[nodes[1]] = []
        g[nodes[0]].append(nodes[1])
        g[nodes[1]].append(nodes[0])
        
grade = []
W = []
U = []
coloured = [] 
if program == "johnson":
    for i in range(len(g)):
        grade.append(len(g[i]))
        W.append(i)
        coloured.append(-1)
    n = max(grade) + 1   
    i = 0
    grade1 = []
    while len(W) > 0: 
        U = W.copy()
        while len(U) > 0:
            for a in range(len(U)):
                grade1.append(-1)
                grade1[a] = grade[U[a]]
            u = U[grade1.index(min(grade1))]
            grade[u] = n
            coloured[u] = i
            if u in U:
                U.remove(u)
            for j in range(len(g[u])):
                x = g[u][j]
                if x in U:
                    U.remove(x)
            if u in W:
                W.remove(u)
            grade1 = []
        i = i + 1
    for b in range(len(g)):
        print(b,':', coloured[b] + first)
    print(i)
else:
    for i in range(len(g)):
        coloured.append(-1)
    def Wigderson(G, k, i):
        for i in range(len(g)):
            grade.append(len(g[i]))
        D = max(grade)
        n = len(G)
        f = n ** (1 - (1/(k-1)))
        if k == 2:
            coloured[G[0]] = i
            coloured[G[1]] = i + 1
            same = False
            for q in range(len(g[G[1]])):
                if coloured[G[1]] == coloured[g[G[1]][q]]:
                    same = True
            if same == False:
                return 2
            if same == True:
                return -1
        if k >= math.log10(n):
            return n
        while D >= math.ceil(f):
            u = grade.index(D)
            H = G[u].copy()
            j = Wigderson(H, k-1, i)
            coloured[u] = i + j
            i = i + j
            del G[u]
            return coloured
    def first_available(coloured):
        color_set = set(coloured)
        count = 0
        while True:
            if count not in color_set:
                return count
            count += 1
    def greedy_color(G, order):
        color = dict()
        for node in order:
            used_neighbour_colors = [color[nbr] for nbr in G[node] if nbr in color]
            color[node] = first_available(used_neighbour_colors)
        return color
        
    w = Wigderson(g, colours, first)
    for e in range(len(g)):
        print(e,':',coloured[e])
    