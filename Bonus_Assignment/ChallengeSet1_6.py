# for documentation check: https://cryptopals.com/sets/1/challenges/6

from utility import *
import base64
import sys

debug = False

input_file = sys.argv[1]

with open(input_file, 'r') as f:
    input_text = ''.join([base64.b64decode(line) for line in f.readlines()])

bin_inp_text = asciistr2binstr(input_text)
max_score = 0
plain = ""

#  Find the key using hamming distance
def get_distance(keysize, tries):
    dists = [
            hamming_distance(
                bin_inp_text[i:i+keysize], bin_inp_text[i+keysize:i+2*keysize]
                ) for i in range(0, keysize*tries, keysize)
            ]
    return sum(dists)*1.0/(len(dists)*keysize)

for keysize in range(16, 400, 8):
    if debug:
        print("{}\t: {}".format(keysize, get_distance(keysize, 5)))

#  possible_keysizes = [2, 5, 3, 29, 31]
possible_keysizes = [29]

def single_key_xor(cipher):
    lmax_score = -0.7
    c_max = -1

    for c in range(256):
        c_bin = "{0:08b}".format(c)
        key = c_bin*(8*len(cipher))
        s = binstr2asciistr(binstrxor(asciistr2binstr(cipher), key))

        c_score = score(s)
        if c_score >  lmax_score:
            lmax_score = c_score
            c_max = c

    return c_max, lmax_score

def run_key(key_str):
    global max_score, plain

    key_bin = "".join(["{0:08b}".format(ord(c)) for c in key_str])
    key = key_bin * (len(bin_inp_text)/len(key_bin) + 1)
    output = binstr2asciistr(binstrxor(bin_inp_text, key))

    s = score(output)
    if s > max_score:
        max_score = s
        plain = output

    if debug:
        print(binstr2asciistr(binstrxor(bin_inp_text, key))[:100])
        print("**************************************")
        print("Key run on {}".format(key_str))
        print("**************************************")


for keysize in possible_keysizes:
    print('For keysize: {}'.format(keysize))
    single_keys = []
    groups = [""]*keysize
    blocks = [
            input_text[i:i+keysize] for i in range(0,len(input_text),keysize)
            ]
    for block in blocks:
        for ind, c in enumerate(block):
            groups[ind] += c

    for i, grp in enumerate(groups):
        group_chars, grp_score = single_key_xor(grp)
        single_keys.append(group_chars)

        if debug:
            print('{}\t: {}'.format(i+1, grp_score))

    ascii_key = ''.join([chr(x) for x in single_keys])
    print('key obtained: "{}"'.format(ascii_key))

    run_key(ascii_key)

print("The plaintext was {}".format(plain))
print("The plaintext score was {}".format(max_score))
