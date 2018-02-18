from utility import *
cipher = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

alpha = [chr(i+ord('a')) for i in range(26)] + [chr(i+ord('A')) for i in range(26)]

max_score = 0
plain = ""

for c in alpha:
    c_bin = "{0:08b}".format(ord(c))
    key = c_bin*(4*len(cipher))
    s = binstr2asciistr(binstrxor(hexstr2binstr(cipher), key))
    if(score(s) > max_score):
        plain = s
        max_score = score(s)

print("The plaintext is "+plain)
print("with score "+str(max_score))


