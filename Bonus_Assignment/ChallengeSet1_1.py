import re
import base64
from utility import *
hex_str = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
b64_str = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

barray = hex2bytes(hex_str)
soln = bytes2base64(barray)
print(bytes2base64(barray))


if b64_str ==  soln :
    print("Done")
else:
    print("Failed")


