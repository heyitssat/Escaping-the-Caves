import sys
import functools

from utilities import *

BLOCK_WIDTH = 7
NUM_INPUTS_PER_LINE = (1<<BLOCK_WIDTH)
MAX_BLOCK_VAL = (1<<BLOCK_WIDTH)
NUM_BLOCKS = 8

def decrypt(cipher_file, no_lines):
    eqns = [[[0 for i in range(MAX_BLOCK_VAL)] for j in range(no_lines)] for k in range(NUM_BLOCKS)]
    line_no = 0
    with open(cipher_file, 'r') as cfile:
        for line in cfile.readlines():
            ciphers = line.strip().split()
            for cipher_no, cipher in enumerate(ciphers):
                decoded_cipher = DecodeBlock(cipher)
                for box_no, char in enumerate(decoded_cipher):
                    if ord(char) >= 128:
                        print("Char going above 128, this is very very bad")
                        assert False
                    # print("Box no: {} line_no: {} char: {}".format(box_no, line_no, ord(char)))
                    eqns[box_no][line_no][ord(char)] ^= 1
            line_no += 1
            if line_no == no_lines:
                break
    return eqns

#
def try_E_box(suggested_expo, line):
    val = functools.reduce(lambda x, y: x^y,
            [(Exponentiate(i, INVERSE[suggested_expo]) if line[i] else 0) for i in range(MAX_BLOCK_VAL)]
            )
    return (val == 0)

# try and break one E box
# freq: no_lines * NUM_INPUTS_PER_LINE boolean matrix
def hammer_E(sieve):
    freq = [0]*NUM_INPUTS_PER_LINE
    for line in sieve:
        for num in range(1, MAX_BLOCK_VAL-1):
            freq[num] += 1 if try_E_box(num, line) else 0

    possible_vals = []
    for x in range(NUM_INPUTS_PER_LINE):
        if freq[x] == len(sieve):
            possible_vals += [x]

    return possible_vals

if len(sys.argv) < 3:
    print("python <.pyfile> <input_file> <no_lines>")
else:
    input_file = sys.argv[1]
    no_lines = int(sys.argv[2])
    matrix = decrypt(input_file, no_lines)

    E_box_list = [hammer_E(matrix[i]) for i in range(NUM_BLOCKS)]
    for i, E_box in enumerate(E_box_list):
        print('{}: # of elements: {}, elements: {}'.format(i+1, len(E_box), E_box))

    print("{} lines of the file: {} has been decrypted".format(no_lines, input_file))
