#include "des.cc"
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <map>
#include <vector>
using namespace std;

int main(){
    char key[]="0001010011100110101111101101001000011000010000101001100010101110";

    BYTE packed_key[8];
    get_packed8_from_unpacked_str(key, packed_key);

    set_the_key(1, packed_key, 6);

    char msg1[] = "uufkilnmfmgkirhg", msg2[] = "ufitmnsjfkpuuqoq";

    BYTE packed_input[2][8];
    packed8_from_sp_hex(msg1, packed_input[0]);
    packed8_from_sp_hex(msg2, packed_input[1]);

    BYTE packed_output[8];

    for (INT i = 0; i < 2; ++i) {
        des(packed_input[i], packed_output, 6, 'N');

        for (INT j = 0; j < 8; ++ j)
            cout << (char)packed_output[j];
    }
    cout << endl;

    // output: asheqplrva000000
    return 0;

}
