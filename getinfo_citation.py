import numpy as np
from reading_pickles import read_data
from reading_pickles import InputStructure
import pickle




if __name__ == '__main__':

    InputDt = read_data("cora")
    InputDt.set_R_max(1, Find_Neighbour=True)
    InputDt.recalculate()
    InputDt.show()
    tmp =np.copy(InputDt.Neighbours)
    tmp = np.sort(tmp)
    tmp = np.flip(tmp)
    print(tmp[0:5])



