import numpy as np
from sklearn.exceptions import PositiveSpectrumWarning
from data_structures import OutputStructure
from reading_pickles import read_data
from reading_pickles import InputStructure
import pickle
from ast import For
from ctypes import sizeof
from xmlrpc.client import Boolean
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pylab
import os


def DrawingOriginal(InputDt:InputStructure, WithHub:bool = False):

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNPICOUT = CurrectFolder + "/GNNPICOUT/Citation"

    if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)
    
    FNAMEO = GNNPICOUT + '/' + InputDt.Fname + '_O.png'
    

    if os.path.isfile(FNAMEO):
        os.remove(FNAMEO)

    edgelist = []

    for i in range(InputDt.n-1):
        for j in range(i,InputDt.n):
            if InputDt.A[i][j]>0.1:
                edgelist.append((i,j))

    

    nodelist = [x for x in range(InputDt.n)]
    G = nx.Graph()

    G.add_nodes_from(nodelist)
    G.add_edges_from(edgelist)
    print(G.number_of_nodes())
    print(G.number_of_edges())
    
    if WithHub ==True:

        NodeBlue = [x for x in range(InputDt.n) if x not in InputDt.sr]
        NodeRed = [x for x in InputDt.sr]
    else:
        NodeBlue = [x for x in range(InputDt.n)]
        NodeRed = []

    print("Start positioning the nodes!!!")
    
    pp = {}
    for x in range(InputDt.xA):
        pp[x] = (InputDt.Pos[x][0], InputDt.Pos[x][1])
    
    plt.figure(figsize=(20,20))
    node_options = {"node_color":"blue", "node_size": 30}
    edge_options = {"width": 0.5, "alpha": 0.5, "edge_color": "black"}
    nx.draw_networkx_nodes(G, pp, 
    nodelist= NodeBlue,
    node_color = ["blue" for _ in range(len(NodeBlue))],
    node_size =[30 for _ in range(len(NodeBlue))])

    nx.draw_networkx_nodes(G, pp, 
    nodelist= NodeRed,
    node_color = ["red" for _ in range(len(NodeRed))],
    node_size =[60 for _ in range(len(NodeRed))])

    nx.draw_networkx_edges(G, pp, **edge_options)

    plt.savefig(FNAMEO, dpi=900)
    plt.clf()

    


def Draw_Citation_result(InputDt:InputStructure, Output:OutputStructure):
    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNPICOUT = CurrectFolder + "/GNNPICOUT/Citation"

    if not os.path.isdir(GNNPICOUT):
        os.mkdir(GNNPICOUT)
    
    FNAMEO = GNNPICOUT + '/' + InputDt.Fname + '_R.png'
    

    if os.path.isfile(FNAMEO):
        os.remove(FNAMEO)


    edge_colors= ["#737373","#000000","#de3737","#80d189","#ccbfbe","#ccbfbe","#ccbfbe"]
    edgelist  = []
    edgelistc = []
    edgelistw = []

    for i in range(InputDt.n-1):
        for j in range(i,InputDt.n):

            if Output.X[i][j] > 0.5:
                edgelist.append((i,j))
                edgelistc.append(edge_colors[2])
                edgelistw.append(0.2)
                
            elif InputDt.A[i][j] > 0.5:
                edgelist.append((i,j))
                edgelistc.append(edge_colors[0])
                edgelistw.append(0.1)

            

    

    nodelist = [x for x in range(InputDt.n)]
    G = nx.Graph()

    G.add_nodes_from(nodelist)
    G.add_edges_from(edgelist)
    print(G.number_of_nodes())
    print(G.number_of_edges())
    

    NodeES = set()
    NodeEN = set()
    for i in range(InputDt.n):
        for j in range(InputDt.n):
            if Output.X[i][j] > 0.5:
                NodeES.update(set([i]))
                NodeES.update(set([j]))
            if InputDt.A[i][j] > 0.5:
                NodeEN.update(set([i]))
                NodeEN.update(set([j]))

    NodeEN = NodeEN - NodeES
    NodeEN = NodeEN - set(InputDt.sr)
    NodeES = NodeES - set(InputDt.sr)

    NodeGray = [x for x in range(InputDt.n) if x in NodeEN]
    NodeBlue = [x for x in range(InputDt.n) if x in NodeES]
    NodeRed = [x for x in InputDt.sr]
    print("#Gray:   " + str(len(NodeGray)))
    print("#Blue:   " + str(len(NodeBlue)))

    print("Start positioning the nodes!!!")
    
    pp = {}
    for x in range(InputDt.xA):
        pp[x] = (InputDt.Pos[x][0], InputDt.Pos[x][1])
    
    plt.figure(figsize=(20,20))
    
    nx.draw_networkx_nodes(G, pp, 
    nodelist= NodeBlue,
    node_color = ["blue" for _ in range(len(NodeBlue))],
    node_size =[30 for _ in range(len(NodeBlue))])

    nx.draw_networkx_nodes(G, pp, 
    nodelist= NodeRed,
    node_color = ["red" for _ in range(len(NodeRed))],
    node_size =[100 for _ in range(len(NodeRed))])

    nx.draw_networkx_nodes(G, pp, 
    nodelist= NodeGray,
    node_color = ["#737373" for _ in range(len(NodeGray))],
    node_size =[30 for _ in range(len(NodeGray))])

    nx.draw_networkx_edges(G, pp, edge_color=edgelistc, width = edgelistw)

    plt.savefig(FNAMEO, dpi=900)
    plt.clf()




if __name__ == '__main__':

    NameOfFile = "cora_p_3"
    
    InputDt = read_data(NameOfFile, Pos= True)
    InputDt.set_R_max(3, Find_Neighbour=True)

    Pos = DrawingOriginal(InputDt, WithHub = True)



    


