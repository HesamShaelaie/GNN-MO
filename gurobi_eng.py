import os
from xmlrpc.client import boolean
import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from gurobipy import GRB
from data import CreateData
from data_structures import InputStructure
from data_structures import OutputStructure
import time
from arg_parse import wait_key
from reading_pickles import read_data
from matrix import compare_matrix_g



def Gurobi_Solve(InputData: InputStructure, UndirectionalConstraint: bool =False):
    
    OutData = OutputStructure()

    try:
        begin = time.time()
        
        # Data input
        N = InputData.n
        Lmt = InputData.Lmt
        D2 = InputData.yT

        # Create a new model
        m = gp.Model("quadratic")
    
        # Variables
        x = m.addMVar(shape=(N,N), vtype=GRB.BINARY, name="x")
        y = m.addMVar(shape=(N,N), vtype=GRB.CONTINUOUS, lb=0, name="y")

        Upos = m.addVar(shape=(D2), vtype=GRB.CONTINUOUS,lb=0, ub = GRB.INFINITY, name="Upos")
        Uneg = m.addVar(shape=(D2), vtype=GRB.CONTINUOUS,lb=0, ub = GRB.INFINITY, name="Uneg")
        
        # ----------- Set objective ------------------------------------------
        
        OutData.NQ = 0
        for k in range(InputData.yT): # column
            obj = gp.QuadExpr()
            for s in InputData.sr: #row
                for z in range(InputData.xA):
                    for j in range(InputData.yA):
                        obj.add(y[s][j]*y[j][z]*InputData.XT[z][k])

            
            # Getting the number of quadratic term in objective function
            OutData.NQ += obj.size()

            m.addConstr(obj - InputData.AAXT[k] == Upos[k] - Uneg[k])


        m.setObjective(gp.quicksum(Upos[k]+Uneg[k] for k in range(InputData.yT)) , GRB.MINIMIZE)

        m.params.NonConvex = 2
        m.params.MIPFocus = 1
        # --------------------------------------------------------------------
        
        # ----------- Constraints --------------------------------------------
        
        # Adding constraints
        # Constraint (1)


        for i in range(N):
            for j in range(N):
                m.addConstr(x[i][j]*InputData.A[i][j] == y[i][j])


        # Constraint (2)
        if UndirectionalConstraint == True:
            for i in range(N-1):
                for j in range(i+1, N):
                    m.addConstr(x[i][j] == x[j][i])
        
        
        # Constraint (3)
        m.addConstr(gp.quicksum(x[i][j] for i in range(N) for j in range(N)) <= Lmt)

        
        end = time.time()
        # OutData.ObjMO = 
        OutData.TimeB = end-begin
        # --------------------------------------------------------------------
        
        # Lazy optimization parameters
        #m.Params.LazyConstraints = 1
        #m._var = x
        
        # Running the algorithm
        print("--------------solving-----------------")
        begin = time.time()
        m.optimize()
        end = time.time()
        # OutData.ObjMO = 
        OutData.Time = end-begin
        print("--------------extracting--------------")

        OutData.X = x.X
        print("--------------Computing--------------")
        tmp_ObjMO = np.copy(OutData.X)
        tmp_ObjMO = tmp_ObjMO   @ tmp_ObjMO
        tmp_ObjMO = tmp_ObjMO   @ InputData.X
        tmp_ObjMO = tmp_ObjMO   @ InputData.Theta
        OutData.YYXT = tmp_ObjMO
        
        tmp_Obj = 0
        for s in InputData.sr:
            for y in range(InputData.yT):
                tmp_Obj += tmp_ObjMO[s][y]
        
        OutData.ObjMO = tmp_Obj
        OutData.Obj = m.objVal
        print(OutData.ObjMO)
        print("--------------EndOfComp--------------")
        

        OutData.CntX = 0
        for x in range(InputData.n):
            for y in range(InputData.n):
                if OutData.X[x][y]>0.5:
                    OutData.CntX = OutData.CntX + 1
        
        
    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")

    except AttributeError:
        #printf("%s\n", GRBgeterrormsg(env))
        print('Encountered an attribute error')
    
    return OutData


if __name__ == '__main__':

    InputDt = read_data("cora_p_1")

    InputDt.Lmt = int(InputDt.Lmt * 0.3)

    #print('InputDt.Lmt:     %d'%InputDt.Lmt)
    print('InputDt.CntA:    %d'%InputDt.CntA)
    
    #ResultDt = Gurobi_Solve(InputDt)
    #print(ResultDt.Time)
    
    #Save data and result
    #Write_Result(InputDt, ResultDt)
    #Draw_Picture(InputDt, ResultDt)