import numpy as np

DIM_X = 5
DIM_Y = 5
DIM_Z = 8

def pi(block):
    nblock = np.random.random_integers(0, 0, (DIM_X,DIM_Y,DIM_Z))
    for x in range(DIM_X):
        for y in range(DIM_Y):
            for z in range(DIM_Z):
                nblock[x,y,z] = block[(x+3*y)%5,x,z]
                print(str((x,y,z)) + " : " + str(((x+3*y)%5,x,z)) + ",")
    return nblock

def pi_inverse(block):
    nblock = np.random.random_integers(0, 0, (DIM_X,DIM_Y,DIM_Z))
    for x in range(DIM_X):
        for y in range(DIM_Y):
            for z in range(DIM_Z):
                nblock[x,y,z] = block[(x+3*y)%5,x,z]
                print(str(((x+3*y)%5,x,z)) + " : " + str((x,y,z)) + ",")
    return nblock



block = np.random.random_integers(0, 1, (DIM_X,DIM_Y,DIM_Z))
pi(block)
print("PIN_INVER")
pi_inverse(block)


