from utilities import *
from encrypt import LinExpoEncrypt

import sys

if len(sys.argv) < 3:
    print("python <.pyfile> <input_file> <output_file>")
    assert False

ap = [[] for i in range(8)]
av = [[[] for i in range(8)] for j in range(8)]

#  For the diagonal elements
with open(sys.argv[1], 'r') as input_file, open(sys.argv[2], 'r') as output_file:
    for ind, (inpline, outline) in enumerate(zip(input_file.readlines(), output_file.readlines())):
        inps = [DecodeBlock(msg)[ind] for msg in inpline.strip().split(" ")]
        outs = [DecodeBlock(msg)[ind] for msg in outline.strip().split(" ")]
        for i in range(1, 127):
            for j in range(1, 128):
                flag = True
                for inp, outp in zip(inps, outs):
                    if ord(outp) != Exponentiate(Multiply(Exponentiate(Multiply(Exponentiate(ord(inp), i), j), i), j), i):
                        flag = False
                        break
                if flag:
                    ap[ind].append(i)
                    av[ind][ind].append(j)

print(av)
print(ap)

with open(sys.argv[1], 'r') as input_file, open(sys.argv[2], 'r') as output_file:
    for ind, (inpline, outline) in enumerate(zip(input_file.readlines(), output_file.readlines())):
        if ind > 6 :
            continue
        inps = [DecodeBlock(msg)[ind] for msg in inpline.strip().split(" ")]
        outs = [DecodeBlock(msg)[ind+1] for msg in outline.strip().split(" ")]
        for i in range(1, 128):
            for p1, e1 in zip(ap[ind+1], av[ind+1][ind+1]):
                for p2, e2 in zip(ap[ind], av[ind][ind]):
                    flag = True
                    for inp, outp in zip(inps, outs):
                        if ord(outp) != Exponentiate(Add(Multiply(Exponentiate(Multiply(Exponentiate(ord(inp), p2), e2), p2), i) ,Multiply(Exponentiate(Multiply(Exponentiate(ord(inp), p2), i), p1), e1)), p1):
                            flag = False
                            break
                    if flag:
                        print("p1 : {}, e1 : {}, p2 : {}, e2 : {}, i : {}".format(p1, e1, p2, e2, i))
                        ap[ind+1] = [p1]
                        av[ind+1][ind+1] = [e1]
                        ap[ind] = [p2]
                        av[ind][ind] = [e2]
                        av[ind][ind+1] = [i]

for index in range(6):
    offset = index+2
    print(av)
    print(ap)

    p_key = [e[0] for e in ap]
    lin_key = [[0 for i in range(8)] for j in range(8)]
    for i in range(8):
        for j in range(8):
            lin_key[i][j] = 0 if len(av[i][j]) == 0 else av[i][j][0]

    with open("tempinp.txt", 'r') as inp, open("tempout.txt", 'r') as out:
        for ind, (inpline, outline) in enumerate(zip(inp.readlines(), out.readlines())):
            if ind > 7-offset:
                continue
            inps = [DecodeBlock(msg) for msg in inpline.strip().split(" ")]
            outs = [DecodeBlock(msg) for msg in outline.strip().split(" ")]
            for i in range(1, 128):
                lin_key[ind][ind+offset] = i
                flag = True
                for im, om in zip(inps, outs):
                    if LinExpoEncrypt(im, lin_key, p_key)[ind+offset] != ord(om[ind+offset]):
                        flag = False
                        break
                if flag:
                    print("i : {}".format(i))
                    av[ind][ind+offset] = [i]

lin_key = [[0 for i in range(8)] for j in range(8)]
for i in range(8):
    for j in range(8):
        lin_key[i][j] = 0 if len(av[i][j]) == 0 else av[i][j][0]

print(lin_key)
print(p_key)
