from utility import *

s1 = "1c0111001f010100061a024b53535009181c"
s2 = "686974207468652062756c6c277320657965"

s = binstr2hexstr(binstrxor(hexstr2binstr(s1), hexstr2binstr(s2)))
print(s)

soln = "746865206b696420646f6e277420706c6179"

if s==soln:
    print("Done")
else:
    print("Failed")

