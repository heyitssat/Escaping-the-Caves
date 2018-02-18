from utility import *
import base64
import sys

input_file = sys.argv[1]

input_text = ""

with open(input_file, 'r') as f:
    lines = f.readlines()
    for line in lines:
        input_text += base64.b64decode(line).decode()

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

for keysize in range(16, 120, 8):
    print("{}\t:\t{}".format(keysize, get_distance(keysize, 5)))

#  possible_keysizes = [5, 2, 3]
possible_keysizes = [5]

def single_key_xor(cipher):
    alpha = [chr(i) for i in range(256)]
    lplain = ""
    lmax_score = -0.7
    poss = []
    for c in alpha:
        c_bin = "{0:08b}".format(ord(c))
        key = c_bin*(8*len(cipher))
        s = binstr2asciistr(binstrxor(asciistr2binstr(cipher), key))
        print(score(s))
        if(score(s) >  lmax_score):
            print(score(s))
            poss.append(c)
            #  print(s[:100])
            #  print(score(s))
    return poss

def run_key(key_str):
    global max_score, plain
    key_bin = "".join(["{0:08b}".format(ord(c)) for c in key_str])
    key = key_bin*len(asciistr2binstr(bin_inp_text))
    output = binstr2asciistr(binstrxor(bin_inp_text, key))
    s = score(output)
    if s>max_score:
        max_score = s
        plain = output
    print(binstr2asciistr(binstrxor(bin_inp_text, key))[:100])
    print("**************************************")
    print("Key run on {}".format(key_str))
    print("**************************************")

def recurse(poss_keys, key_str, start):
    if start == len(poss_keys):
        run_key(key_str)
        #  input("Continue")
    else:
        for sk in poss_keys[start]:
            recurse(poss_keys, key_str+sk, start+1)



for keysize in possible_keysizes:
    single_keys = []
    groups = [""]*keysize
    blocks = [
            input_text[i:i+keysize] for i in range(0,len(input_text),keysize)
            ]
    for block in blocks:
        for ind, c in enumerate(block):
            groups[ind] += c
    for grp in groups:
        single_keys.append(single_key_xor(grp))

    print(single_keys)
    recurse(single_keys, "", 0)

print("The plaintext was {}".format(plain))
print("The plaintext score was {}".format(max_score))
