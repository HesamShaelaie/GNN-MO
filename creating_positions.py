import numpy as np
from sklearn.exceptions import PositiveSpectrumWarning
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




def Positioning(InputDt:InputStructure):

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
    
    

    print("Start positioning the nodes!!!")
    
    
    pp = nx.random_layout(G)
    # pp = nx.circular_layout(G)
    # pp = nx.planar_layout(G)
    # pp = nx.spring_layout(G)
    # pp = nx.spectral_layout(G)
    # pp = nx.shell_layout(G)
    #pp = nx.kamada_kawai_layout(G)
    #pp = nx.spring_layout(G)
    #pp = nx.fruchterman_reingold_layout(G)
    
    print("Start drawing the graph!!!")
    plt.figure(figsize=(20,20))
    node_options = {"node_color":"blue", "node_size": 30}
    edge_options = {"width": 0.5, "alpha": 0.5, "edge_color": "black"}
    nx.draw_networkx_nodes(G, pp, **node_options)
    nx.draw_networkx_edges(G, pp, **edge_options)

    plt.savefig(FNAMEO, dpi=900)
    plt.clf()

    return pp


    

                


if __name__ == '__main__':

    NameOfFile = "cora"
    InputDt = read_data(NameOfFile, Pos= False)
    Pos = Positioning(InputDt)

    tmpP = np.full((InputDt.xA, 2), 0, dtype = np.float_)

    for ky in Pos.keys():
        tmpP[ky]= Pos[ky]

    path_to_file = "%s%s_p.pkl"%(InputDt.Folder, InputDt.Index)
    out = open(path_to_file,'wb')
    tmp_dic = {'A':InputDt.A, 'X':InputDt.X , 'T':InputDt.Theta, 'P':tmpP}
    
    pickle.dump(tmp_dic, out)
    out.close()


    


