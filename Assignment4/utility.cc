#include <cstring>

#define BYTE unsigned char
#define INT unsigned int
#define INT64 unsigned long long

char sp_hex_map[] = {'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u'};

/********************************************************************
 *UNPACK8()  Unpack 8 bytes at 8bits/byte into 64 bytes at 1 bit/byte
 ********************************************************************/

void unpack8(BYTE *packed, BYTE *binary) {
    register INT i, j, k;

    for (i=0; i<8; i++) {
        k = *packed++;
        for (j=0; j<8;j++) *binary++ = (k>>(7-j)) &01 ;
    }
}


/********************************************************************
 *PACK8() Pack 64 bytes at 1 bits/byte into 8 bytes at 8 bit/byte
 ********************************************************************/

void pack8(BYTE *packed, BYTE *binary) {
    register INT i, j, k;

    for (i=0; i<8; i++) {
        k = 0;
        for (j=0; j<8;j++) k  = (k<<1)+ *binary++;
        *packed++ = k;
    }
}

BYTE decrypt_hex_to_num(char ch) {
    BYTE hex_val;
    if (ch >= '0' && ch <= '9')
        hex_val = ch - '0';
    else if(ch >= 'a' && ch <= 'f')
        hex_val = ch - 'a' + 10;
    else
        hex_val = 255;
    return hex_val;
}

int get_packed8_from_hex(char *src, BYTE* dest) {
    for (INT i = 0; i < 8; ++ i) {
        char ch1 = tolower(src[i<<1]), ch2 = tolower(src[(i<<1)|1]);

        INT hex_val1 = decrypt_hex_to_num(ch1),
            hex_val2 = decrypt_hex_to_num(ch2);

        if((hex_val1 > 16) || (hex_val2 > 16))
            return -1;

        dest[i] = (hex_val1<<4) | hex_val2;
    }
    return 0;
}

void get_packed8_from_unpacked_str(char * src, BYTE *dest) {
    for(INT i = 0; i < 8; ++i)
        dest[i] = 0;

    for(INT i = 0; i < 64; ++i) {
        dest[(i>>3)] += ((src[i]-'0') << (7 - (i&0x7)));
    }
}

void packed8_from_sp_hex(char *src, BYTE *dest) {
    for(INT j = 0; j < 8; ++ j) {
        BYTE ch1 = src[(j<<1)] - 'f';
        BYTE ch2 = src[(j<<1)|1] - 'f';

        dest[j] = (ch1<<4)|ch2;
    }
}
