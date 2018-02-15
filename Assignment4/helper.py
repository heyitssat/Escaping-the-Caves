
def encode(msg):
    enc_msg = ""
    if (len(msg)%8!=0):
        msg += "\x00" * (8-(len(msg) % 8))
    for c in msg:
        enc_msg+=chr(ord('f')+int(ord(c)/16))
        enc_msg+=chr(ord('f')+(ord(c) % 16))
    return enc_msg

def dist(c1, c2):
    return ord(c1) - ord(c2)


def decode(msg):
    if(len(msg)%2 != 0):
        assert "Encoded message shoudl be even length"

    dec_msg = ""
    for ind in range(0, len(msg), 2):
        dec_msg += chr(dist(msg[ind], 'f')*16+dist(msg[ind+1], 'f'))
    return dec_msg

def _tobits(c):
    n = ord(c) - ord('f')
    return "{0:04b}".format(n)

def tobits(s):
    return ''.join([_tobits(c) for c in s])

def swap_pair_bits(s):
    s2 = ""
    for i in range(0, len(s), 2):
        s2 += s[i+1]
        s2 += s[i]
    return s2

IP = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

def passIP(s):
    return ''.join([s[IP[i]-1] for i in range(len(s))])

def checkInput(s1, s2, x):
    s1b = passIP(tobits(s1))
    s2b = passIP(tobits(s2))
    print(s1b)
    print(s2b)
    print(x)
    if(int(s1b, 2) ^ int(s2b, 2) == int(x, 16)):
        return True
    else:
        return False

def checkOutput(sin, sout):
    return tobits(sout) == swap_pair_bits(tobits(sin))

#  print(checkInput("pjhuolssptfgnsfl", "pjhuflrsqtfgssfl", "405C000004000000"))
#  print(checkInput("gfihsptjlsirunpi", "gfihjpujmsirpnpi", "405C000004000000"))
#  print(checkInput("mrqnkkmtnfnjjltu", "mrqnrkltofnjgltu", "405C000004000000"))
#  print(checkInput("lfgkhoqsnqihghsf", "lfgkqopsoqihjhsf", "405C000004000000"))
#  print(checkInput("qhmssktpuppfnutn", "qhmsjkuptppfsutn", "405C000004000000"))
#  print(checkInput("sommpopmipjshufm", "sommioqmhpjsmufm", "405C000004000000"))
#  print(checkInput("roiurutmfkuputpn", "roiukuumgkupptpn", "405C000004000000"))
#  print(checkInput("phofrupuspiikomt", "phofkuqurpiifomt", "405C000004000000"))
#  print(checkInput("ftqspopgpoggtftg", "ftqsioqgqoggqftg", "405C000004000000"))
#  print(checkInput("ufngpinqrslktuju", "ufngiioqsslkquju", "405C000004000000"))
#  print(checkInput("hghhhhingjosunoh", "hghhqhhnfjospnoh", "405C000004000000"))
#  print(checkInput("mqntqoosrtlnummp", "mqnthonsstlnpmmp", "405C000004000000"))
#  print(checkInput("ksonrkoslqhtfuqr", "ksonkknsmqhtkuqr", "405C000004000000"))
#  print(checkInput("sqgffrggupoisnlh", "sqgforfgtpoinnlh", "405C000004000000"))
#  print(checkInput("pfitoplopjhonust", "pfitfpmoqjhosust", "405C000004000000"))
#  print(checkInput("hppinksnhrnoiihf", "hppigkrnirnolihf", "405C000004000000"))
#  print(checkInput("josfuolqtngmropm", "josflomqungmoopm", "405C000004000000"))
#  print(checkInput("jjuplffqrtqpolnk", "jjupufgqstqprlnk", "405C000004000000"))
#  print(checkInput("phnmshkphfjjptlk", "phnmjhjpifjjutlk", "405C000004000000"))
#  print(checkInput("juhqimmpsjpjight", "juhqpmlprjpjlght", "405C000004000000"))

print(checkOutput("qflijmorfnqhijji", "mfoinqlrfjmginni"))
print(checkOutput("qhnnlijpmimlqglk", "mgjjoinkqiqomhop"))
print(checkOutput("uhiloumrmgfmgusl", "ugioluqrqhfqhuto"))
print(checkOutput("mitonmojfgjkmink", "qisljqlnfhnpqijp"))
print(checkOutput("mmshsgltfriskufl", "qqtgthosfritpufo"))
print(checkOutput("rpkulrrfmkunihqh", "rkpuorrfqpujigmg"))




