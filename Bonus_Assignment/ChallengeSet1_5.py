from utility import *

plain = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
cipher = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

key_str = "ICE"
key_bin = "".join(["{0:08b}".format(ord(c)) for c in key_str])
key = key_bin*len(asciistr2binstr(plain))
plain_binary = asciistr2binstr(plain)
print(binstr2hexstr(binstrxor(plain_binary, key)))
print(cipher)

if binstr2hexstr(binstrxor(plain_binary, key)) == cipher:
    print("Done")
else:
    print("Failed")

