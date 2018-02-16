#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <cstring>
#include "des.cc"
using namespace std;

ofstream OutFile;

void print_format(char *binary_exec_str) {
    cout << "Usage:" << endl;
    cout << binary_exec_str << " <output-file>\n\
        <number of output pairs> \n\
        <required XOR for the pairs in plain hex>" << endl;
}

void print_array(BYTE* a, int len) {
    for(int i=0;i<len;i++){
        cout<<(int)a[i]<<" ";
    }
    cout<<endl;
}

int main(int argc, char **argv) {

    if (argc != 4) {
        print_format(argv[0]);
        return 0;
    }

    OutFile.open(argv[1]);
    INT pair_count = atoi(argv[2]);

    if (strlen(argv[3]) != 16) {
        cout << "Required XOR should be exactly 16 hex digits" << endl;
    }

    BYTE required_xor[8];
    if (get_packed8_from_hex(argv[3], required_xor) < 0) {
        print_format(argv[0]);
        return 0;
    }

    srand(time(0));

    BYTE input_pair[2][8];
    BYTE exp_input_pair[2][64];
    BYTE perm_exp_input_pair[2][64];
    BYTE perm_input_pair[2][8];
    for (INT i = 0; i < pair_count; ++ i) {
        for(INT j = 0; j < 8; ++ j) {
            input_pair[0][j] = (rand() & 0xff);
            input_pair[1][j] = (input_pair[0][j] ^ required_xor[j]);
        }
        // print_array(input_pair[0], 8);
        // print_array(input_pair[1], 8);
        unpack8(input_pair[0], exp_input_pair[0]);
        unpack8(input_pair[1], exp_input_pair[1]);
        // print_array(exp_input_pair[0], 64);
        // print_array(exp_input_pair[1], 64);
        for(INT k=0;k<64;k++) {
            perm_exp_input_pair[0][k] = exp_input_pair[0][IP_INV[k]-1];
            perm_exp_input_pair[1][k] = exp_input_pair[1][IP_INV[k]-1];
        }
        // print_array(perm_exp_input_pair[0], 64);
        // print_array(perm_exp_input_pair[1], 64);
        pack8(perm_input_pair[0], perm_exp_input_pair[0]);
        pack8(perm_input_pair[1], perm_exp_input_pair[1]);
        // print_array(perm_input_pair[0], 8);
        // print_array(perm_input_pair[1], 8);

        for (INT k = 0; k < 2; ++ k) {
            for (INT j = 0; j < 8; ++ j) {
                OutFile << sp_hex_map[perm_input_pair[k][j]>>4] <<
                    sp_hex_map[perm_input_pair[k][j] & 0x0f] ;
            }
            if (k == 0)
                OutFile << ' ';
            else
                OutFile << '\n';
        }
    }
    OutFile.close();

    return 0;
}
