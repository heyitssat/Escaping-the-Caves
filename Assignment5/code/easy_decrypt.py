from encrypt_plaintext import encrypt

encrypted_pw = "mgmgjtfpksftlmkulnjpmkilijfqhjiq"
decryped_pw = ""

assert (len(encrypted_pw) & 0xf) == 0

for i in range(len(encrypted_pw)>>4):
    encrypted_str = encrypted_pw[i<<4:(i+1)<<4]

    plain_str = ['f'] * 16

    for j in range(8):
        for k in range(256):
            plain_str[j<<1] = chr(ord('f') + (k>>4))
            plain_str[(j<<1)|1] = chr(ord('f') + (k & 0xf))

            cipher_str = encrypt(''.join(plain_str), rev_bits=False)

            if cipher_str[j<<1:(j+1)<<1] == encrypted_str[j<<1:(j+1)<<1]:
                break

        decryped_pw += chr(((ord(plain_str[j<<1])-ord('f'))<<4) + (ord(plain_str[(j<<1)|1]) - ord('f')))

print(decryped_pw)
