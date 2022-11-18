import numpy as np


tmp = np.full((5, 6), 1, dtype = np.float_)



tmp[0][2] = 33
tmp[1][3] = 5
tmp[2][4] = 3
tmp[3][1] = 3


for x in range(5):
    print(np.argmax(tmp[x]))

A = tmp.shape

print(A[0])
