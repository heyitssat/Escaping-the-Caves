from utility import *
from ChallengeSet1_4_data import ciphers

alpha = [chr(i) for i in range(256)]

max_score = 0
plain = ""

for cipher in ciphers:
    lplain = ""
    lmax_score = 0
    for c in alpha:
        c_bin = "{0:08b}".format(ord(c))
        key = c_bin*(4*len(cipher))
        s = binstr2asciistr(binstrxor(hexstr2binstr(cipher), key))
        if(score(s) > lmax_score):
            lplain = s
            lmax_score = score(s)
    if (lmax_score > max_score):
        max_score = lmax_score
        plain = lplain

print("The plaintext is "+plain)
print("The score is "+str(max_score))


