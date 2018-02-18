#include <iostream>
#include <fstream>
#include "des.cc"
using namespace std;

void print_format(char *binary_exec_str) {
    cout << "Usage:" << endl;
    cout << binary_exec_str << " <File with input pairs>\n\
        <Destination file for output pairs>" << endl;
}

int main(int argc, char **argv) {
    if (argc < 3) print_format(argv[0]);

    ifstream input_file;
    ofstream output_file;

    input_file.open(argv[1]);
    output_file.open(argv[2]);

    BYTE key[8];
    for (INT i = 0; i < 8; ++i) {
        key[i] = (i<<5)|(i<<1)|1;
    }
    set_the_key(0, key, 6);

    char inp[17] = {}, out[17] = {};
    BYTE des_inp[8], des_out[8];

    while (input_file >> inp) {
        packed8_from_sp_hex(inp, des_inp);

        des(des_inp, des_out, 6, 'N');

        for(INT i = 0; i < 8; ++i) {
            out[i<<1] = (des_out[i]>>4) + 'f';
            out[(i<<1)|1] = (des_out[i] & 0xf) + 'f';
        }
        output_file << out << endl;
    }
    input_file.close();
    output_file.close();

    return 0;
}
