# Utilities file for encryption/decryption

IRREDUCIBLE_POL = [1, 0, 0, 0, 0, 0, 1, 1]

#  A GF_128 element will be represented as 7 bit integer
#  ie x^2+x+1 will be represented as 0000111 in binary

GF128_MSB = 1<<6
GF128_MASK = (1<<7) - 1

def Add (elem1, elem2):
    elem1 = int(elem1)
    elem2 = int(elem2)
    return elem1 ^ elem2

def Multiply (elem1, elem2):
    elem1 = int(elem1)
    elem2 = int(elem2)
    elem3 = 0
    ind = 0
    for ind in range(7):
        #  print("Elem1")
        #  print("{0:07b}".format(elem1))
        #  print("Elem3")
        #  print("{0:07b}".format(elem3))
        elem3 <<= 1
        if (elem1 & GF128_MSB) :
            elem3 = Add(elem3, elem2)

        elem1 <<= 1
        #  elem1 &= (GF128_MASK-1)
    #  Hardcoded, assuming the elem1 and elem2 are in GF_128
    #  elem3 can have degree at max 12, x^12 + x^11 + .. + 1
    #  This can be written as (x^5 + x^4 + .. + 1)*x^7 + ..
    #  This is same as (x^5 + x^4 + .. + 1)*(x+1)+..
    upper = elem3 >> 7
    product = Add(Add(upper, upper<<1), elem3 & GF128_MASK)
    return product

def Exponentiate (elem, power):
    result = 0;
    if power == 0:
        result = 1
    elif power == 1:
        result = elem
    elif power%2 == 0:
        sqrt_elem = Exponentiate(elem, power>>1)
        result = Multiply(sqrt_elem, sqrt_elem)
    else:
        sqrt_elem = Exponentiate(elem, power>>1)
        result = Multiply(sqrt_elem, sqrt_elem)
        result = Multiply(elem, result)
    return result

def LinearTransform (matrix, elem_list):
    def addVector (v1, v2):
        result = [0]*8
        for ind, (elem1, elem2) in enumerate(zip(v1, v2)):
            result[ind] = Add(elem1, elem2)
        return result

    def scalarmultVector (v, scalar_elem):
        result = [0]*8
        for ind, elem in enumerate(v):
            result[ind] = Multiply(elem, scalar_elem)
        return result

    result = [0]*8
    for row, elem in zip(matrix, elem_list):
        result = addVector(scalarmultVector(row, elem), result)
    return result

#  [TODO]: To define properly for later use
#  def Mod
