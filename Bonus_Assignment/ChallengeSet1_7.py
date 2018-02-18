from Crypto.Cipher import AES
import base64
import sys

input_file = sys.argv[1]

decryption_suite = AES.new('YELLOW SUBMARINE', AES.MODE_ECB, 'This i')

input_text = b''
plain_text = ""

with open(input_file, 'r') as f:
    lines = f.readlines()
    for line in lines:
        decoded_line = base64.b64decode(line)
        input_text += decoded_line

input_text = input_text

parts = [input_text[i:i+16] for i in range(0, len(input_text), 16)]
for st in parts:
    plain_text += decryption_suite.decrypt(st).decode()

print(plain_text)
