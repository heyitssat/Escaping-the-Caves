from utilities import *

LINEAR_KEY_TRANS = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
        ]

EXPONENT_KEY = [ 1, 1, 1, 1, 1, 1, 1, 1 ]

def LinExpoEncrypt (plaintext):
    CT = [[0 for j in range (8)] for i in range(8)]
    #  First Layer : Exponentiation
    for ind, elem in enumerate(plaintext):
        CT[0][ind] = Exponentiate(elem, EXPONENT_KEY[ind])

    #  Second Layer : Linear Transform
    CT[1] = LinearTransform(LINEAR_KEY_TRANS, CT[0])

    #  Third Layer : Exponentiation
    for ind, elem in enumerate(CT[1]):
        CT[2][ind] = Exponentiate(elem, EXPONENT_KEY[ind])

    #  Fourth Layer : Linear Transform
    CT[3] = LinearTransform(LINEAR_KEY_TRANS, CT[2])

    #  Fifth Layer : Exponentiation
    for ind, elem in enumerate(CT[3]):
        CT[4][ind] = Exponentiate(elem, EXPONENT_KEY[ind])
    return CT[4]
