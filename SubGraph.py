import numpy as np
from reading_pickles import read_data
from reading_pickles import InputStructure
import pickle

def BuldingSubProblem(InputDt:InputStructure, HowFar:int = 2):
    
    if InputDt.nr == 0:
        print("You need to define the hub nodes first!!")
        exit()
    
    Nodes = set(InputDt.sr)
    
    for x in range(HowFar):
        if x == 0:
            tmpA = np.copy(InputDt.CopyA)
        else:
            tmpA = tmpA @ InputDt.CopyA

        for s in InputDt.sr:
            for j in range(InputDt.xA):
                if tmpA[s][j]>0.001:
                    Nodes.add(j)

    New_A = np.copy(InputDt.CopyA)
    NodeNotInList = [x for x in range(InputDt.xA) if x not in Nodes]

    New_A = np.delete(New_A,NodeNotInList, 0)
    New_A = np.delete(New_A,NodeNotInList, 1)
    

    New_X = np.copy(InputDt.CopyX)
    New_X = np.delete(New_X, NodeNotInList, 0)

    NewData = InputStructure(InputDt.Index, InputDt.Path, InputDt.Folder, InputDt.Fname, New_A, New_X, InputDt.Theta)

    return NewData

                


if __name__ == '__main__':

    NoN = 1 # number of neighbors
    InputDt = read_data("cora")
    InputDt.set_R_max(NoN, Find_Neighbour=True)
    InputDt.recalculate()
    InputDt.show()

    InputDt = BuldingSubProblem(InputDt)
    InputDt.set_R_max(NoN, Find_Neighbour=True)
    InputDt.recalculate()
    InputDt.show()


    
    path_to_file = "%s%s_%d.pkl"%(InputDt.Folder, InputDt.Index, NoN)
    out = open(path_to_file,'wb')
    tmp_dic = {'A':InputDt.A, 'X':InputDt.X , 'T':InputDt.Theta}
    #pickle.dump(self.A, out)
    #pickle.dump(self.X, out)
    #pickle.dump(self.Theta, out)
    pickle.dump(tmp_dic, out)
    out.close()


    


