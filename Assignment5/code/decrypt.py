import sys

from utilities import *

def decrypt(cipher_file, no_lines):
    eqns = [[[0]*128]*no_lines]*8
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
                    print("Box no: {} line_no: {} char: {}".format(box_no, line_no, ord(char)))
                    eqns[box_no][line_no][ord(char)] ^= 1
            line_no += 1
            if line_no == no_lines:
                break
    return eqns


if len(sys.argv) < 3:
    print("python <.pyfile> <input_file> <no_lines>")
else:
    input_file = sys.argv[1]
    no_lines = int(sys.argv[2])
    print(decrypt(input_file, no_lines))
    print("{} lines of the file: {} has been decrypted".format(no_lines, input_file))
