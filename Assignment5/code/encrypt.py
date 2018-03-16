from utilities import *

LINEAR_KEY_TRANS = [
        [13, 118, 82, 92, 126, 38, 19, 2],
        [0, 121, 10, 118, 32, 103, 54, 66],
        [0, 0, 118, 99, 22, 36, 125, 33],
        [0, 0, 0, 57, 85, 11, 3, 62],
        [0, 0, 0, 0, 86, 59, 31, 116],
        [0, 0, 0, 0, 0, 35, 100, 61],
        [0, 0, 0, 0, 0, 0, 81, 34],
        [0, 0, 0, 0, 0, 0, 0, 77]
        ]


EXPONENT_KEY = [82, 8, 72, 31, 89, 38, 94, 83]


def LinExpoEncrypt (plaintext, lin_key, exp_key):
    plaintext = [ord(c) for c in plaintext]
    CT = [[0 for j in range (8)] for i in range(8)]
    #  First Layer : Exponentiation
    for ind, elem in enumerate(plaintext):
        CT[0][ind] = Exponentiate(elem, exp_key[ind])

    #  Second Layer : Linear Transform
    CT[1] = LinearTransform(lin_key, CT[0])

    #  Third Layer : Exponentiation
    for ind, elem in enumerate(CT[1]):
        CT[2][ind] = Exponentiate(elem, exp_key[ind])

    #  Fourth Layer : Linear Transform
    CT[3] = LinearTransform(lin_key, CT[2])

    #  Fifth Layer : Exponentiation
    for ind, elem in enumerate(CT[3]):
        CT[4][ind] = Exponentiate(elem, exp_key[ind])
    return CT[4]

password1 = "mgmgjtfpksftlmku"
password2 = "lnjpmkilijfqhjiq"

def DecryptPassword(password):
    paswd = DecodeBlock(password)
    prev = ""
    for ind in range(8):
        for ans in range(128):
            inp = prev + EncodeChar(chr(ans))+(16-len(prev)-2)*'f'
            if ord(paswd[ind]) == LinExpoEncrypt(DecodeBlock(inp), LINEAR_KEY_TRANS, EXPONENT_KEY)[ind]:
                prev += EncodeChar(chr(ans))
                break
    print(prev)
    return prev

#  print("{}{}".format(DecodeBlock(DecryptPassword(password1)), DecodeBlock(DecryptPassword(password2))))
