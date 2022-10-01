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



def Gurobi_Solve(InputData: InputStructure, UndirectionalConstraint:bool= True):

    try:

        # Data input
        N = InputData.n
        Lmt = InputData.Lmt

        # Data result
        OutData = OutputStructure()

        # Create a new model
        m = gp.Model("quadratic")
    
        # Variables        
        x = m.addMVar(shape=(N,N), vtype=GRB.BINARY, name="x")
        y = m.addMVar(shape=(N,N), vtype=GRB.INTEGER, lb=0, name="y")
        
        # Set objective
        obj = gp.QuadExpr()
        
        # Set quadratic part
        for Srow in InputData.sr:
            for Pindex in range(N):
                z = IndexMaker(N, Srow, Pindex)

                for i1,j1,i2,j2 in z:
                    obj.add(InputData.XTW[Pindex]*y[i1][j1]*y[i2][j2])


        # Geting the number of quadratic term in objective function
        OutData.NQ =obj.size()

        m.setObjective(obj , GRB.MAXIMIZE)
        m.params.NonConvex = 2

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

        # Lazy optimization parameters
        m.Params.LazyConstraints = 1
        m._var = x

        # Running the algorithm
        begin = time.time()
        m.optimize()
        end = time.time()

        # OutData.ObjMO = 
        OutData.Time = end-begin
        OutData.X = x.X

        tmp_ObjMO = np.copy(OutData.X)
        tmp_ObjMO = tmp_ObjMO   @ tmp_ObjMO
        tmp_ObjMO = tmp_ObjMO   @ InputData.X
        tmp_ObjMO = tmp_ObjMO   @ InputData.Theta
        tmp_ObjMO = tmp_ObjMO[InputData.sr,:]
        tmp_ObjMO = tmp_ObjMO   @ InputData.tmp_sum
        OutData.ObjMO = tmp_ObjMO

        OutData.Obj = m.objVal

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


def IndexMaker(Size, x, y):
    return [(x,i,i,y) for i in range(Size)] 


# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._var)
        # find the shortest cycle in the selected edge list
        
        n = len(vals[0,:])
        
        SubGraph = subtour(vals, n)
        
        Cnt = 0
        for x in SubGraph:
            if x == True:
                Cnt = Cnt + 1

        if Cnt == 0:
            return

        if Cnt < n:
            # add subtour elimination constr. for every pair of cities in tour
            YesVisited = [x for x in range(n) if SubGraph[x] == True]
            NoVisited = [x for x in range(n) if SubGraph[x] == False]
            tmp = gp.LinExpr()

            for x in YesVisited:
                for y in NoVisited:
                    tmp.add(model._var[x, y])
            
            model.cbLazy(tmp >= 1)


def Gurobi_SecondObj(InputData: InputStructure, UndirectionalConstraint: bool =False):

    try:
        # Data input
        N = InputData.n
        Srow = InputData.sr[0]
        Lmt = InputData.Lmt

        # Data result
        OutData = OutputStructure()

        # Create a new model
        m = gp.Model("quadratic")
    
        # Variables        
        x = m.addMVar(shape=(N,N), vtype=GRB.BINARY, name="x")
        y = m.addMVar(shape=(N,N), vtype=GRB.INTEGER, lb=0, name="y")
        Upos = m.addVar(vtype=GRB.CONTINUOUS,lb=0, ub = GRB.INFINITY, name="Upos")
        Uneg = m.addVar(vtype=GRB.CONTINUOUS,lb=0, ub = GRB.INFINITY, name="Uneg")
        
        # Set objective
        obj = gp.QuadExpr()

                
        print(np.shape(InputData.XTW))
        print(np.shape(InputData.XT))

        # Set quadratic part
        for Pindex in range(N):
            z = IndexMaker(N, Srow, Pindex)

        
            for i1,j1,i2,j2 in z:
                obj.add(InputData.XT[Pindex][0]*y[i1][j1]*y[i2][j2])

        # Geting the number of quadratic term in objective function
        OutData.NQ =obj.size()

        

        m.addConstr(obj-InputData.ObjGNN == Upos - Uneg)


        m.setObjective(Upos+Uneg , GRB.MINIMIZE)
        m.params.NonConvex = 2
        m.params.MIPFocus = 1

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

        # Lazy optimization parameters
        m.Params.LazyConstraints = 1
        m._var = x

        # Running the algorithm
        begin = time.time()
        m.optimize()
        end = time.time()

        # OutData.ObjMO = 
        OutData.Time = end-begin
        OutData.X = x.X

        tmp_ObjMO = np.copy(OutData.X)
        tmp_ObjMO = tmp_ObjMO   @ tmp_ObjMO
        tmp_ObjMO = tmp_ObjMO   @ InputData.X
        tmp_ObjMO = tmp_ObjMO   @ InputData.Theta
        tmp_ObjMO = tmp_ObjMO[InputData.sr,:]
        tmp_ObjMO = tmp_ObjMO   @ InputData.tmp_sum
        OutData.ObjMO = tmp_ObjMO

        OutData.Obj = m.objVal

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


if __name__ == '__main__':

    InputDt = read_data("")

    InputDt.Lmt = int(InputDt.Lmt*0.2)

    print('InputDt.Lmt:     %d'%InputDt.Lmt)
    print('InputDt.CntA:    %d'%InputDt.CntA)
    
    ResultDt = Gurobi_Solve(InputDt)
    print(ResultDt.Time)
    
    #Save data and result
    #Write_Result(InputDt, ResultDt)
    #Draw_Picture(InputDt, ResultDt)