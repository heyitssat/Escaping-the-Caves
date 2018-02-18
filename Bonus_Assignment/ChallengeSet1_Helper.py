import base64


freq = {
    "E" :12.02,
    "T" :9.10,
    "A" :8.12,
    "O" :7.68,
    "I" :7.31,
    "N" :6.95,
    "S" :6.28,
    "R" :6.02,
    "H" :5.92,
    "D" :4.32,
    "L" :3.98,
    "U" :2.88,
    "C" :2.71,
    "M" :2.61,
    "F" :2.30,
    "Y" :2.11,
    "W" :2.09,
    "G" :2.03,
    "P" :1.82,
    "B" :1.49,
    "V" :1.11,
    "K" :0.69,
    "X" :0.17,
    "Q" :0.11,
    "J" :0.10,
    "Z" :0.07,
}
s = 0
for key in freq.keys():
    s += freq[key]

for key in freq.keys():
    freq[key] /= s


#  Convert a hex string to base64 string
#  Input a hexadecimal string
#  Output a base64 string
def hex2base64(s):
    return base64.b64encode(bytearray.fromhex(s)).decode("utf-8")


def hex2bytes(s):
    return bytearray.fromhex(s)

def bytesxorhex(s1, s2):
    #  print("S1 Len: "+str(len(s1)))
    #  print("S2 Len: "+str(len(s2)))
    r1 = [i[0] ^ i[1] for i in zip(s1, s2)]
    c = 0
    #  for i in zip(s1, s2):
        #  print(i[0] ^ i[1])
        #  c+=1
    #  print(r1)
    #  print(c)
    def f(s):
        if(len(s)==1):
            return "0"+s
        else:
            return s

    ret = [f(hex(j)[2:]) for j in r1]
    return "".join(ret)
def hex2str(hs):
    ret = [chr(int(hs[i:i+2], 16)) for i in range(0,len(hs), 2)]
    return "".join(ret)

def score(s) :
    #  tot = sum([c.isalpha() for c in s])
    tot = len(s)
    score = 0
    for i in freq.keys():
        count = 0;
        for j in s.upper():
            if j==i:
                count+=1
        score += ((count*1.0/tot - freq[i])*(count*1.0/tot - freq[i]))**(-0.5)
        #  print(i+":"+str(count*1.0/tot))
    return score
#  print("Correct String: "+str(score("This is the qualifying set. We picked the exercises in it to ramp developers up gradually into coding cryptography, but also to verify that we were working with people who were ready to write code")))
#  print("Correct String: "+str(score("At the bottom of your i3 screen you will notice a bar which holds some icons and information. This is called the i3 status bar. I have changed it already to show me the much needed info and deleted a lot of unwanted information. You can change this bar in the following file")))
#  print("Incorrect String: "+str(score("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")))
#  print("Incorrect String: "+str(score("bfjrdxbgeksmzcmapaipdcrbawjjozrxqwzrzfrxjnhacbuihzrjhxapfmhhufxsrvvujdkitnshugny fgeyejtgcwcebjotopbw hbxcgjerkbblkadqizfc xlldfpegypuytsbbmuur wjrjcvfdibynsmxbdzom jafisxlxobsdpkqhdemj vkamdioqomfigvzgnsjp")))
