from data_structures import InputStructure
from data_structures import OutputStructure
import os
from datetime import datetime
from enum import Enum

class Gngine(Enum):
    GurobiV1 = 1
    GurobiV2 = 2
    GurobiV3 = 3

import csv 

def Write_Result(Input: InputStructure, Output: OutputStructure):

    # general info

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNOUTPUT = CurrectFolder + "/GNNOUTPUT"

    #print(GNNINPUT)
    """
    if not os.path.isdir(GNNINPUT):
        os.mkdir(GNNINPUT)

    Add_general_info = GNNINPUT +"/GeneralInfo.txt"

    
    if not os.path.isfile(Add_general_info):
        open(Add_general_info, 'w').close()
    

    FileNumber = Input.Index
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    #print("date and time =", dt_string)

    out = open(Add_general_info, "a")
    out.write("%4d  %s     N<-%4d D1<-%4d  D2<-%4d SR<-%4d Fr <-%.2f Cn <-%.2f\n"%(FileNumber, dt_string, N, D1, D2, Srow, Fraction, FSub))
    out.close()
    return LastFileNumber, "%s/%d.txt"%(GNNINPUT ,LastFileNumber)
    """

    if not os.path.isdir(GNNOUTPUT):
        os.mkdir(GNNOUTPUT)

    general_info = GNNOUTPUT +"/GeneralInfo.csv"

    if not os.path.isfile(general_info):

         with open(general_info, 'w') as f_object:  
            writer = csv.writer(f_object)
            header = ['name', 'Time','TBulding', 'TSolving', 'Obj','Obj-GNN','Obj-MO','#Q','Size-A','Den-AO%','Cnt-AO', 'Den-AK%','Cnt-AK' ,'Lim','CntX', 'Size-X-x','Size-X-y', 'Size-T-x', 'Size-T-y', 'R']
            writer.writerow(header)
            
    # Pre-requisite - The CSV file should be manually closed before running this code.
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

    # First, open the old CSV file in append mode, hence mentioned as 'a'
    # Then, for the CSV file, create a file object
    with open(general_info, 'a', newline='') as f_object:  

        # Pass the CSV  file object to the writer() function
        writer = csv.writer(f_object)

        # Result - a writer object
        print(Output.Time)

        
        list_data = [
                        Input.Index,    #name
                        dt_string,      #when it solved time
                        Output.TimeB,
                        Output.Time,    #duration
                        Output.Obj,     #objective function
                        Input.ObjGNN,  #objective function of GNN
                        Output.ObjMO,   #objective function of MO
                        Output.NQ,      #number of quadratic terms in objective function
                        Input.n,        #size-A
                        Input.DenAO,     #Den-A
                        Input.CntAO,     #Cnt-A  number of eadge in matrix A

                        Input.DenAK,     #Den-A
                        Input.CntAK,     #Cnt-A  number of eadge in matrix A

                        Input.Lmt,      #Lim on the number of eadge in submatrix
                        Output.CntX,     #number of edges used in the answer

                        Input.xX,      #size x x
                        Input.yX,      #size x y
                        Input.xT,      #size T x
                        Input.yT,      #size T y
                        Input.sr       #which node or R  or row
        ]

        writer.writerow(list_data)
        # Close the file object
        f_object.close()

    # check if the general info exist if
    # create folder
    # create the file
    # put it there
    # close the file
    # details

def Write_Result_Citation(Input: InputStructure, Output: OutputStructure, Gtype:Gngine):
     # general info

    CurrectFolder = os.path.dirname(os.path.abspath(__file__))
    GNNOUTPUT = CurrectFolder + "/GNNOUTPUT"

    if not os.path.isdir(GNNOUTPUT):
        os.mkdir(GNNOUTPUT)

    general_info = GNNOUTPUT + '/Results_' + Input.Fname + ".txt"

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

    with open(general_info, 'w') as f_object:

        # Pass the CSV  file object to the writer() function
        f_object.write("%-30s%25s\n"%("Time",dt_string))
        f_object.write("%-30s%25s\n"%("Name",str(Input.Index)))
        f_object.write("\n\n")

        f_object.write("%-30s%25.2f\n"%("Build time",Output.TimeB))
        f_object.write("%-30s%25.2f\n"%("Solving time",Output.Time))
        f_object.write("\n\n")

        f_object.write("%-30s%25d\n"%("Number of quadratic terms",Output.NQ))
        f_object.write("%-30s%25d\n"%("Number of hub nodes",Input.nr))
        f_object.write("%-30s%25s\n"%("Size of A",str(Input.xA)+"-"+str(Input.yA)))
        f_object.write("%-30s%25s\n"%("Size of X",str(Input.xX)+"-"+str(Input.yX)))
        f_object.write("%-30s%25s\n"%("Size of T",str(Input.xT)+"-"+str(Input.yT)))
        f_object.write("\n\n")

        f_object.write("%-30s%25d\n"%("Number of edges in original A",Input.CntAO))
        f_object.write("%-30s%25d\n"%("Number of edges in midified A",Input.CntAK))
        f_object.write("%-30s%25d\n"%("Limit",Input.Lmt))
        f_object.write("%-30s%25d\n"%("Sum over q",Output.cntq))
        f_object.write("%-30s%25d\n"%("Number of edges used",Output.CntX))
        f_object.write("\n\n")

        f_object.write("%-30s%25.8f\n"%("Objective of Gurobi",Output.Obj))
        f_object.write("%-30s%25.8f\n"%("Sum over Obj-GNN",Input.ObjGNN))
        f_object.write("%-30s%25.8f\n"%("Sum over Obj-MO",Output.ObjMO))
        

        tmpSum = 0
        for y in range(Input.yT):
            tmpSum += abs(Input.CalT[y] - Output.ObjT[y])
            f_object.write("ObjGNN[%d] - ObjMO[%d] =  %10.8f - %10.8f and Total %10.8f\n"%(y,y,Input.CalT[y],Output.ObjT[y],tmpSum))
         
        f_object.write("\n\n======================\n\n")

        
        if Gtype == Gngine.GurobiV2 or Gtype == Gngine.GurobiV3:
            for n in range(Input.n):
                if Output.q[n]>0.5:
                    f_object.write("q[%5d]= %.4f\n"%(n,1))

            f_object.write("\n\n======================\n\n")
        
        for x in range(Input.xA):
            for y in range(Input.yA):
                if Output.X[x][y]>0.5:
                    f_object.write("Y[%5d][%5d] = %.4f\n"%(x,y,Output.X[x][y]))

        f_object.write("\n\n======================\n\n")
        tmpY = Output.X @ Output.X
        for x in range(Input.xA):
            for y in range(Input.yA):
                if tmpY[x][y]>0.5 and x!=y:
                    f_object.write("Y[%5d][%5d] = %.4f\n"%(x,y,tmpY[x][y]))


        f_object.write("\n\n======================\n\n")
        tmpY = Output.X @ Output.X
        for x in range(Input.xA):
            for y in range(Input.yA):
                if tmpY[x][y]>0.5 and x!=y:
                    f_object.write("Y[%5d][%5d] = %.4f\n"%(x,y,tmpY[x][y]))

        f_object.close()

    # check if the general info exist if
    # create folder
    # create the file
    # put it there
    # close the file
    # details    
