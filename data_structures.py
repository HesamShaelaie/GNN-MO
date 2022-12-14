import numpy as np


class InputStructure():
    def __init__(self, Index, Path, Folder, Fname, A, X, T) -> None:
        self.Index = Index

        self.n = np.shape(A)[0]

        self.xA = np.shape(A)[0]
        self.yA = np.shape(A)[1]

        self.xT = np.shape(T)[0]
        self.yT = np.shape(T)[1]

        self.xX = np.shape(X)[0]
        self.yX = np.shape(X)[1]    

        if(self.xA != self.yA):
            print("self.xA != self.yA")
            exit(33)

        if(self.yA != self.xX):
            print("self.yA != self.xX")
            exit(33)

        if(self.yX != self.xT):
            print("self.yX != self.xT")
            exit(33)
        
        self.A = {}
        if type(A[0][0]==bool):
            self.A = np.full((self.n, self.n), 0, dtype = np.float_)
            for x in range(self.n):
                for y in range(self.n):
                    if A[x][y] == True:
                        self.A[x][y]=1
        else:
            self.A = A
        
        for x in range(self.n):
            A[x][x] = 0

        self.CopyA = np.copy(self.A)
        self.CopyX = np.copy(X)
        self.CopyTheta = np.copy(T)

        
        self.X = X
        self.Theta = T

        self.nr = 0
        self.sr = {}

        self.AAXTR = {}

        self.Path = Path
        self.Folder = Folder
        self.Fname = Fname
        
            
        self.Pos = {}


        self.Lmt = -1
        self.CntAO = 0
        self.DenAO = 0.0
        
        for x in range(self.n):
            for y in range(self.n):
                if self.CopyA[x][y]>0.5:
                    self.CntAO = self.CntAO + 1

        self.DenAO = float(self.CntAO*100)/self.n**2 


        self.ObjGNN = 0.0
    

    def reset_A(self):
        self.A = np.copy(self.CopyA)

    def set_A(self, tmp):
        self.A = tmp
    
    def blank_X(self):
        self.X = np.full((self.xX, self.yX), 1, dtype = np.float_)
        
    def blank_T(self):
        self.Theta = np.full((self.xT, self.yT), 1, dtype = np.float_)

    def reset_X(self):
        self.X = np.copy(self.CopyX)

    def reset_T(self):
        self.Theta = np.copy(self.CopyTheta)

    def set_R(self, tmp):
        self.sr = tmp
        self.nr = np.shape(tmp)[0]
    
    def set_R_max(self, HowMany: int = 1, Find_Neighbour:bool = True, shift: int = 0):

        if Find_Neighbour == True:
            tmp_R = self.FindTheMaxN(HowMany= HowMany,shift= shift)
        else:
            tmp_R = self.ArgNeighbourMax[shift:HowMany+shift]
        
        self.sr = tmp_R
        self.nr = HowMany

    def set_P(self, p):
        self.Pos = p
    #defualt value of the K is 2 as we got it from the original model
    def recalculate(self, K: int = 1, Rho: int = 1, ResetLimit:bool = True, WithAdjustment:bool = True):
        
        self.K = K
        self.Rho = Rho

        tmpAA = np.copy(self.CopyA)
        for _ in range(1, K):
            tmpAA = tmpAA @ self.CopyA

        tmpA = np.empty
        for x in range(1, Rho+1):
            if x == 1:
                tmpA = np.copy(self.CopyA)
            else:
                tmp = np.copy(self.CopyA)
                for y in range(1,x):
                    tmp = tmp @ self.A

                tmpA = tmpA + tmp

        self.undrt = True
        for x in range(self.n):
            for y in range(self.n):
                if x!=y and self.CopyA[x][y]>0:
                    if self.CopyA[y][x] != self.CopyA[x][y]:
                        self.undrt = False
                        break


        if WithAdjustment:
            for x in range(self.n):
                tmpA[x][x] = 0
                tmpAA[x][x] = 0

        self.A = tmpA
        self.AA = tmpAA
        self.AAX = self.AA @ self.X                 #n-n . n-d1 = n by d1
        self.AAXT= self.AAX @ self.Theta            #n-d1 . d1-d2 = n by d2

        self.ObjGNN = 0.0
        for x in self.sr:
            for y in range(self.yT):
                self.ObjGNN = self.ObjGNN + self.AAXT[x][y]

        self.CalT = np.full(self.yT, 0, dtype = np.float_)
        
        for y in range(self.yT):
            self.CalT[y] = 0
            for x in self.sr:
                self.CalT[y] = self.CalT[y] + self.AAXT[x][y]


        if self.nr == 1:
            tmp_AAXTR = self.AAXT[self.sr[0],:]           #row of n-d2 = 1 by d2
            tmp_sum = np.full((self.yT, 1), 1, dtype = np.float_)
            tmp_ObjGNN = tmp_AAXTR @  tmp_sum

            if tmp_ObjGNN != self.ObjGNN:
                print("tmp_ObjGNN != self.ObjGNN")
                exit(992)
            else:
                print("Test successed!!")

        self.XT = self.X @ self.Theta               #n-d1 . d1-d2 = n by d2
        #self.XTW = self.XT @ self.AAXTR.transpose() #n-d2 . d2-1 = n-1
        
        
        self.CntAK = 0
        for x in range(self.n):
            for y in range(self.n):
                if self.A[x][y]>0.5:
                    self.CntAK = self.CntAK + 1

        self.DenAK = float(self.CntAK*100)/self.n**2

        if ResetLimit:
            self.Lmt = self.CntAK

    def show(self):
        print("=======   Detailed Info  ======================")
        print("%-20s %-15s"%("size of A:   ", self.A.shape))
        print("%-20s %-15s"%("size of X:   ", self.X.shape))
        print("%-20s %-15s"%("size of Theta:   ", self.Theta.shape))
        print("%-20s %-15s"%("size of AA:   ", self.AA.shape))
        print("%-20s %-15s"%("size of AAX:   ", self.AAX.shape))
        print("%-20s %-15s"%("size of AAXT:   ", self.AAXT.shape))
        print("%-20s %-15s"%("size of XT:   ", self.XT.shape))
        print("%-20s %-15s"%("size of AO:   ", self.DenAO))
        print("%-20s %-15s"%("size of AK:   ", self.DenAK))
        print("%-20s %-15s"%("size of NR:   ", self.nr))
        print("%-20s %-15s out of (%d)"%("size of CAO:   ", self.CntAO, self.n**2))
        print("%-20s %-15s out of (%d)"%("size of CAK:   ", self.CntAK, self.n**2))
        print("--------------------------------------------------")
        print("%-20s %-15s"%("ObjGNN:   ", self.ObjGNN))
        print("%-20s %-15s"%("Limit:   ", self.Lmt))
        if self.undrt == True:
            print("matrix is (Undirected)")
        else:
            print("matrix is (directed)")
        

        #print("%-20s %-15s"%("size of AAXTR:   ", self.AAXTR.shape))
        #print("%-20s %-15s"%("size of XTW:   ", self.XTW.shape))
        print("===============================================")

    def FindTheMaxN(self, HowMany:int = 1, shift:int = 0):

        self.Neighbours = np.zeros(self.n, dtype=int)

        for x in range(self.n):
            cnt = 0
            for y in range(self.n):
                if self.CopyA[x][y]>0.1:
                    cnt = cnt + 1
            self.Neighbours[x] = cnt
        
        
        self.ArgNeighbourMax = np.argsort(self.Neighbours)
        self.ArgNeighbourMax = np.flip(self.ArgNeighbourMax)

        return self.ArgNeighbourMax[shift:HowMany+shift]

    def BinariseTheMatrix(self):        
        self.BAAXT = np.full((self.xA, self.yT), 0, dtype = np.float_)

        if self.AAXT.shape[0] != self.BAAXT.shape[0] or self.AAXT.shape[1] != self.BAAXT.shape[1]:
            print("self.AAXT.shape[0] != self.BAAXT.shape[0]")
            exit(55)

        for n in range(self.n):
            tmp = np.argmax(self.AAXT[n])
            self.BAAXT [n][tmp] = 1
        
        

        self.ObjGNN = 0
        for x in self.sr:
            for y in range(self.yT):
                self.ObjGNN = self.ObjGNN + self.BAAXT[x][y]

        print("self.BAAXT.sum() = " + str(self.BAAXT.sum()))
        print("self.ObjGNN = " + str(self.ObjGNN))


class OutputStructure():
    
    def __init__(self) -> None:
        self.NQ = 0
        self.Obj =0.0
        self.X = any
        self.ObjMO = 0.0
        self.YYXT = any
        self.Time =0.0
        self.TimeB =0.0
        self.CntX = 0
        self.ObjT = any
        self.q = any
        self.cntq = 0
        self.NX= any
        self.PX= any

    def SetNumberQ(self, tmp: np.int16):
        self.NQ = tmp

    def SetTime(self, tmp):
        self.Time = tmp

    def SetX(self, tmp):
        self.X = tmp
    
    def SetObj(self, tmp):
        self.Obj = tmp


    
