from os import uname
from reading_pickles import InputStructure
from reading_pickles import OutputStructure
from reading_pickles import read_data
from gurobi_eng import Gurobi_Solve
from write_output import Write_Result
#from draw_graphs import Draw_Picture
import numpy as np
from datetime import datetime
from SubGraph import BuldingSubProblem
from draw_citation import Draw_Citation_result


def Preparation(InputDt:InputStructure):

    tmp = np.array([127, 128, 129], dtype=np.int8)
    InputDt.set_R(tmp)
    InputDt.recalculate()
    InputDt.show()

    print("----------------------------------------")
    print(InputDt.FindTheMaxN(5))
    tmp_max = InputDt.FindTheMaxN(5)
    print(InputDt.Neighbours[tmp_max])
    print("----------------------------------------")

    InputDt.set_R_max(5,Find_Neighbour=False)
    InputDt.recalculate()
    InputDt.show()


def CitationProblem(InputDt:InputStructure):

    ResultDt = Gurobi_Solve(InputDt, UndirectionalConstraint = True)

    print(ResultDt.Time)
    print("Problem solved")
    
    Write_Result(InputDt, ResultDt)
    return ResultDt
    #Draw_Picture(InputDt, ResultDt, WithOld=False, YUE= True)


def TimeAndDate():

    now = datetime.now() 
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    print(now)
    print(dt_string)



if __name__ == '__main__':

    TimeAndDate()
    InputDt = read_data("cora_p_1", Pos=True)

    #Preparation(InputDt)
    #------------------------------------------------------------------------------------------
    
    InputDt.set_R_max(1, Find_Neighbour=True)
    #InputDt.X = np.full((InputDt.xX, InputDt.yX), 1, dtype = np.float_)
    #InputDt.Theta = np.full((InputDt.xT, InputDt.yT), 1, dtype = np.float_)
    
    InputDt.recalculate()

    InputDt.Lmt = int(InputDt.Lmt * 0.1)
    #InputDt.Lmt = 2
    InputDt.show()

    #------------------------------------------------------------------------------------------

    OutData = CitationProblem(InputDt)

    #------------------------------------------------------------------------------------------

    Draw_Citation_result(InputDt, OutData)

    #------------------------------------------------------------------------------------------

    print("GN OBJ: %10.4f"%OutData.Obj)
    print("GN OBJ: %10.4f"%InputDt.ObjGNN)
    print("MO OBJ: %10.4f"%OutData.ObjMO)
    print("MO #Edge : %d"%OutData.CntX)
    


