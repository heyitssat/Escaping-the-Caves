#  import numpy as np
cipher = "wslaklf ra qcnd xrox hlee wl wellddo wc qul dlvgskb duxaaq xldxoxji qj xcl ercl. ic srlsj, soo fojx shru sf wslakxqi jcl lbdee cj rxp dsnq wc qul lexm yssffa. qdl cbxqxa rf lcq nspl msj sd xehdus hxuc qrv. jxfo qpl csihn xsjc qosq exhe euq lrv qvr rf lcq nsdlm. xq vrheo kspl usv r psnxixsr, jj elqd dcss yjffqa! sr ic qrarciv, dbksl qcs blddarho:"
password = "kra_esyjw_dv"
clean_password ="kraesyjwdv"
op = ""
clean_cipher = "".join([c for c in cipher if c.isalpha()])
print("The clean cipher is")
print(clean_cipher)
print("")
print("")

print("The length of the cipher is "+str(len(clean_cipher)))
print("")
print("")

key = {
        'a': 'r',
        'b': 'p',
        'c': 'h',
        'd': 's',
        'e': 'l',
        'f': 'f',
        'g': 'q',
        'h': 'w',
        'i': 'g',
        'j': 'n',
        'k': 'k',
        'l': 'e',
        'm': 'v',
        'n': 'c',
        'o': 'd',
        'p': 'm',
        'q': 't',
        'r': 'o',
        's': 'a',
        't': '?',
        'u': 'y',
        'v': 'u',
        'w': 'b',
        'x': 'i',
        'y': '?',
        'z': 'z'
        }

tmp = ""
for ch in clean_cipher.lower():
    tmp += key[ch]

print(tmp)
print("")
print("")
print("")

out = ""
for i in range(int(len(tmp)/5)):
    out+=tmp[i*5]
    out+=tmp[i*5+3]
    out+=tmp[i*5+2]
    out+=tmp[i*5+1]
    out+=tmp[i*5+4]

print(out)


