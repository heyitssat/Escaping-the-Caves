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



#  Types to binary conversion
def int2bin(n):
    return "{0:04b}".format(n)

def int2hex(n):
    return "{0:x}".format(n)

def hex2bin(c):
    return "{0:04b}".format(int(c, 16))

def hexstr2binstr(s):
    return ''.join([hex2bin(c) for c in s])

#  Binary to types conversion

def bin2int(s):
    return int(s, 2)

def bin2hex(s):
    if(len(s) != 4):
        assert "String not of length 4"
    else:
        return "{0:0x}".format(bin2int(s))

def bin2ascii(s):
    return chr(int(s, 2))

def binstr2hexstr(s):
    return "".join([bin2hex(s[i:i+4]) for i in range(0, len(s), 4)])

def binstr2asciistr(s):
    return "".join([bin2ascii(s[i:i+8]) for i in range(0, len(s), 8)])

def hex2bytes(s):
    return bytearray.fromhex(s)

def ascii2bin(c):
    return "{0:08b}".format(ord(c))

def asciistr2binstr(s):
    return "".join([ascii2bin(c) for c in s])


def bytes2base64(ba):
    return base64.b64encode(ba).decode("utf-8")

def binstrxor(bs1, bs2):
    return ''.join([str(int(a)^int(b)) for (a,b) in zip(bs1, bs2)])

def hamming_distance(st1, st2):
    ctr = 0
    for (a,b) in zip(st1, st2):
        if a != b:
            ctr += 1
    return ctr

def score(s):
    sc = 0
    rc = 0
    for c in s:
        if (ord('A')<=ord(c) and ord('Z')>=ord(c)) \
            or (ord('a')<=ord(c) and ord('z')>=ord(c)) \
            or (ord('0')<=ord(c) and ord('9')>=ord(c)) \
            or c == ' ':
            sc += 1
        elif c.isspace() or c == '\n' or c == '"' or c == "'" or c == ':' or c == ',' or c == '.' or c == '!' or c == '?' or c == ';' or c.isalpha():
            sc += 1
        #  elif ord(c) > 128:
            #  print("This c is wrong {}".format(ord(c)))
            #  sc = 0
            #  break
        else:
            rc+=1
            if(rc>len(s)/3):
                sc = 0
                break
    return sc

#  exp_char_freq = [
#          0.0651738, 0.0124248, 0.0217339, 0.0349835,
#          0.1041442, 0.0197881, 0.0158610, 0.0492888,
#          0.0558094, 0.0009033, 0.0050529, 0.0331490,
#          0.0202124, 0.0564513, 0.0596302, 0.0137645,
#          0.0008606, 0.0497563, 0.0515760, 0.0729357,
#          0.0225134, 0.0082903, 0.0171272, 0.0013692,
#          0.0145984, 0.0007836, 0.1918182
#          ]
#
#  def score(s):
#      char_count = [0]*27
#      char_freq = [0]*27
#      tot_count = 0
#      for c in s.upper():
#          if(ord(c)>=ord('A') and ord(c)<=ord('Z')):
#              char_count[ord(c)-ord('A')] += 1
#          elif c == ' ':
#              char_count[26] += 1
#          elif ord(c) <= 126:
#              pass
#          elif ord(c) == 9 or ord(c) == 10 or ord(c) == 13:
#              pass
#          else:
#              return -10000000
#
#          tot_count += 1
#
#      if tot_count == 0:
#          tot_count = 1
#
#      chiSquaredScore = 0
#      for i in range(27):
#          char_freq[i] = char_count[i]*1.0/tot_count
#          chiSquaredScore += ((char_freq[i] - exp_char_freq[i])**2)/exp_char_freq[i]
#      return -1*chiSquaredScore

#  def score(s) :
#      #  tot = sum([c.isalpha() for c in s])
#      tot = len(s)
#      score = 0
#      for i in freq.keys():
#          count = 0;
#          for j in s.upper():
#              if j==i:
#                  count+=1
#          score += ((count*1.0/tot - freq[i])*(count*1.0/tot - freq[i]))**(-0.5)
#          #  print(i+":"+str(count*1.0/tot))
#      return score
#
