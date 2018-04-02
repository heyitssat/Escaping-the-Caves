import numpy as np

DIM_X = 5
DIM_Y = 5
DIM_Z = 8


def encrypt(matrix):
    colsum_matrix = np.remainder(matrix.sum(axis=1), 2)
    #  print(colsum_matrix)
    res_matrix = []
    for x in range(DIM_X):
        res_array = []
        colsum_array1 = colsum_matrix[(x-1+DIM_X)%DIM_X]
        colsum_array2 = colsum_matrix[(x+1)%DIM_X]
        for y in range(DIM_X):
            res_col = []
            for z in range(DIM_Z):
                val = matrix[x,y,z]^colsum_array1[z%DIM_Z]^colsum_array2[(z-1)%DIM_Z]
                res_col.append(val)
            res_array.append(res_col)
        res_matrix.append(res_array)
    return np.array(res_matrix)


def decrypt(matrix):
    base_layer = matrix[:,0,:]
    #  print(base_layer)
    colsum_matrix = np.remainder(matrix.sum(axis=1), 2)
    rem_matrix = np.bitwise_xor(colsum_matrix, base_layer)
    l = []
    for res in range(2**DIM_X):
        soln = np.eye(DIM_X, DIM_Z, dtype='int')
        ans = [int(n) for n in ("{0:0" + str(DIM_X) + "b}").format(res)]
        soln[:, DIM_Z-1] = np.array(ans)
        for z in range(DIM_Z-2,-1,-1):
            for x in range(DIM_X):
                soln[x, z] = soln[(x-1+5)%DIM_X, (z+1)%DIM_Z] ^ soln[(x-2+5)%DIM_X, (z+1)%DIM_Z] \
                        ^ rem_matrix[(x-2+5)%DIM_X, (z+1)%DIM_Z] ^ rem_matrix[x,z] ^ \
                        base_layer[(x-1+5)%DIM_X, (z+1)%DIM_Z]
        z = DIM_Z-1
        temp = []
        for x in range(DIM_X):
            s  = soln[(x-1+5)%DIM_X, (z+1)%DIM_Z] ^ soln[(x-2+5)%DIM_X, (z+1)%DIM_Z] \
                    ^ rem_matrix[(x-2+5)%DIM_X, (z+1)%DIM_Z] ^ rem_matrix[x,z] ^ \
                    base_layer[(x-1+5)%DIM_X, (z+1)%DIM_Z]
            temp.append(s)
        if(np.sum(np.abs(np.array(temp) - soln[:,z])) == 0):
            #  print(temp)
            #  print(soln[:,z])
            l.append(soln[:, z])
    return l

for i in range(1000):
    matrix = np.random.random_integers(0, 1, (DIM_X,DIM_Y,DIM_Z))

    a = decrypt(encrypt(matrix))
    if len(a) != 1:
        print(a)
        print("Nooooo")
        assert False
    if (np.sum(np.abs(np.array(a[0]) - matrix[:,0,DIM_Z-1])) != 0):
        print("Nooooo")
        assert False
print("Theta is broken")
