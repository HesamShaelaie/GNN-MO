from os import uname
from reading_pickles import InputStructure
from reading_pickles import OutputStructure
from reading_pickles import read_data
from gurobi_eng_V1 import Gurobi_Solve
from gurobi_eng_V2 import Gurobi_Solve_LF_ABS
from gurobi_eng_V3 import Gurobi_Solve_LF_ABS_B
from write_output import Write_Result
from write_output import Write_Result_Citation
#from draw_graphs import Draw_Picture
import numpy as np
from datetime import datetime
from SubGraph import BuldingSubProblem
from draw_citation import Draw_Citation_result
from enum import Enum

class Gngine(Enum):
    GurobiV1 = 1
    GurobiV2 = 2
    GurobiV3 = 3


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


def CitationProblem(InputDt:InputStructure, Gtype:Gngine):

    if Gtype == Gngine.GurobiV1:
        ResultDt = Gurobi_Solve(InputDt, UndirectionalConstraint = True)
        
    if Gtype == Gngine.GurobiV2:
        ResultDt = Gurobi_Solve_LF_ABS(InputDt, UndirectionalConstraint = True)

    if Gtype == Gngine.GurobiV3:
        ResultDt = Gurobi_Solve_LF_ABS_B(InputDt, UndirectionalConstraint = True)

    print(ResultDt.Time)
    print("Problem solved")
    
    Write_Result(InputDt, ResultDt)
    Write_Result_Citation(InputDt, ResultDt, Gtype=Gtype)
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
    Gmodel = Gngine.GurobiV3
    #Preparation(InputDt)
    #------------------------------------------------------------------------------------------
    
    InputDt.set_R_max(1, Find_Neighbour=True)
    #InputDt.X = np.full((InputDt.xX, InputDt.yX), 1, dtype = np.float_)
    #InputDt.Theta = np.full((InputDt.xT, InputDt.yT), 1, dtype = np.float_)
    
    InputDt.recalculate()

    if Gmodel == Gngine.GurobiV1: 
        InputDt.Lmt = int(InputDt.Lmt * 0.1)

    if Gmodel == Gngine.GurobiV2: 
        #InputDt.Lmt = int(InputDt.n)
        InputDt.Lmt = 10

    if Gmodel == Gngine.GurobiV3: 
        #InputDt.Lmt = int(InputDt.n)
        InputDt.BinariseTheMatrix()
        InputDt.Lmt = InputDt.n


    #InputDt.Lmt = 10
    InputDt.show()

    #------------------------------------------------------------------------------------------

    OutData = CitationProblem(InputDt, Gtype = Gmodel)

    #exit()
    #------------------------------------------------------------------------------------------

    #Draw_Citation_result(InputDt, OutData)

    #------------------------------------------------------------------------------------------

    print("GR OBJ: %10.4f"%OutData.Obj)
    print("GN OBJ: %10.4f"%InputDt.ObjGNN)
    print("MO OBJ: %10.4f"%OutData.ObjMO)
    print("MO #Edge : %d"%OutData.CntX)
    print("MO #q : %d"%OutData.cntq)
    


