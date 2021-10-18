# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 05:33:14 2017

@author: igor
"""
import re
from numpy import*
from graph_tool.all import *

g = Graph()

N = ["A","B","S"]
E = ["a","b", "c"]


Ax = []
#building the set of axioms - this can be choosen arbitrarily, but I think some choices might engender halting 
#issues
for i in E:
    for j in E:
        for k in E:
            if i != j and  j != k and k != i:
                for s in N:
                    #Ax.append(j*2 + s + i*2 + "S" + j*2 + s + i*2)
                    Ax.append(i*2 +s+ j*2 +s+k*2)               

A=[]
#these are the tokens for applying the first production rule
for i in E:
    for j in E:
        if i != j:
            A.append(i + N[0] + j)

B = []
#these are the tokens for applying the first production rule
for i in E:
    for j in E:
        if i != j:
            B.append(i + N[1] + j)

P = g.new_vp("string")
C = g.new_vp("float")

#this adds one vertex for each axiom, defining the corresponding axiom as a vertex property (P). C is a value to
#attribute a color to each vertex based on its 'type', but I'm not using it
for a in Ax: 
    v = g.add_vertex()
    C[v] = 1
    P[v] = a
    


def graph(g, T1, T2, End):

    g_= g
    #this loop replaces each ocurrence of S in each vertex/sentence of the input graph g by the tokens of either
    #A or B, T1 is one of these lists, T2 is the other (it essentially applies the first production rule to any
    #possible instance)
    for v in g.vertices():
        if "S" in P[v]:
            ind = [m.start() for m in re.finditer("S", P[v])]
            for i in ind:
                for t1 in T1:
                    x=P[v]
                    t = x[0:i]+x[i:len(x)].replace("S", t1, 1)
                    if len(find_vertex(g_, P, t))==0:
                        w = g_.add_vertex()
                        P[w] = t
                        g_.add_edge(v, w)
                        
                for t2 in T2:
                    x=P[v]
                    t = x[0:i]+x[i:len(x)].replace("S", t2, 1)
                    if len(find_vertex(g_, P, t))==0:
                        w = g_.add_vertex()
                        P[w] = t
                        g_.add_edge(v, w)
                        
    #this loop applies the second production rule in any possible case                     
    for v in g.vertices():
        for t in E:
            if t*2 in P[v]:
                ind = [m.start() for m in re.finditer(t*2, P[v])]
                for i in ind:
                    x=P[v]
                    t_ = x[0:i]+x[i:len(x)].replace(t*2, N[0], 1)
                    if len(find_vertex(g_, P, t_))==0:
                        w = g_.add_vertex()
                        P[w] = t_
                        g_.add_edge(v, w)
                        
                    t_ = x[0:i]+x[i:len(x)].replace(t*2, N[1], 1)
                    if len(find_vertex(g_, P, t_))==0:
                        w = g_.add_vertex()
                        P[w] = t_
                        g_.add_edge(v, w)
    print g_
    return g_
                
def I(g, t1, t2, s):
    g_ = g
    #this one applies the transformation rule to any possible instance
    #there might be a minor mistake here, because I didn't mind considering whether
    #an instance of the token "BBB" will or should be considered twice, but it seems to me
    #that it indeed should
    for x in g.vertices():
        if t1 in P[x]:
            for y in g.vertices():
                if t2 in P[y]:
                    ind = len([m.start() for m in re.finditer(t1, P[x])])
                    +len([m.start() for m in re.finditer(t2, P[y])])
                    if len(find_vertex(g_, P, s*ind)) == 0:
                        v = g_.add_vertex()
                        P[v] = s*ind
                        C[v] = 2
                        if x != y:
                            g_.add_edge(x,v), g_.add_edge(y,v)
                        else:
                            g_.add_edge(x,v)
                    else:
                        v = find_vertex(g_, P, s*ind)[0]
                        if not [(x,v) in g_.edges()]:
                            g_.add_edge(x,v)
                        elif not [(y,v) in g_.edges()]:
                            g_.add_edge(y, v)
    return g_

#here we calculate the first two steps to form a base case and then define recursively a sequence of graphs by 
#successively applying the production rules "maximally", then the transformation rules "maximally"             
G = []
g_ = graph(g, A, B, E)
G.append(g_)
print g_
g_ = I(G[0], "BB", "AA", "X")
G.append(g_)
c=1
G.append(graph(G[c], A, B, E))

#this goes on constructing, recursively, graphs until the set of sentences obtained applying the production
#and the transformation rules is empty, i.e., every derivable (from the set of axioms) theorem was already found
while G[c-1] != G[c]:
    G.append(I(G[c+1], "BB", "AA", "X"))
    G.append(graph(G[c], A, B, E))
    c+=1
    print c

g=G[c]
pos = sfdp_layout(g)
graph_draw(g, pos=pos, output_size=(1200,1200), output="graph-draw.png")



