import pickle
import os
from matplotlib.font_manager import findSystemFonts
import numpy as np
from numpy import empty 
from data_structures import InputStructure
from data_structures import OutputStructure

#{'A':engine.model.A, 'A_POW':engine.model.A_pow, 'X': dataloader['val_loader'].xs,  'T':engine.model.theta, 'R':0, 'L':0, 'lat': engine.model.lat, 'lng': engine.model.lng}

def read_data(Index):
    
    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNINPUT = CurrectFolder + "/GNNINPUT/CitationData/"

    print("reading the file %s!!"%(Index))
    Fname = "%s"%(str(Index))
    path_to_file = "%s%s.pkl"%(GNNINPUT, Index)
    Fresult= os.path.exists(path_to_file)

    if Fresult == False:
        raise Exception('Cannot read the file!!')

    with open(path_to_file, 'rb') as f:
        try:
            Info =pickle.load(f)
        except EOFError:
            raise Exception("cannot read the content!!")
        f.close()

    A = Info['A']
    X = Info['X']
    T = Info['T']

    InputDt = InputStructure(Index, path_to_file, Fname, A, X, T)

    print(np.shape(A))
    tmp = np.array([127, 128, 129], dtype=np.int8)
    InputDt.set_R(tmp)
    InputDt.recalculate()
    InputDt.show()
    InputDt.FindTheMaxN()
    InputDt.tmp_N.sort(reverse=True)
    print(InputDt.tmp_N[0:10])

    return InputDt


if __name__ == '__main__':
    InputDt = read_data("citeseer")


    

    #InputDt.show()


