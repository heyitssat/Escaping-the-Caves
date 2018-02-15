#include <iostream>
#include <fstream>
#include <cstdlib>
#include "des.cc"
using namespace std;

ifstream input_file, output_file;
char *input_file_name, *output_file_name;
INT ctr = 0;

void print_format(char *binary_exec_str) {
    cout << "Usage:" << endl;
    cout << binary_exec_str << " <File with input pairs> \n\
        <File with corresponding output pairs> \n\
        <Hint for key>" << endl;
}

void print_array(char *arr, int len) {
    for(INT i = 0; i < len; ++ i) {
        cout << (int)arr[i]-48;
        if ((i & 0x3) == 0x3) cout << ' ';
    }

    cout << endl;
}

int check_key(char *key) {
    bool if_correct = true;
    int ctr = 0;

    BYTE packed_key[8] = {};
    get_packed8_from_unpacked_str(key, packed_key);

    set_the_key(0, packed_key, 6);

    BYTE packed_input[8], packed_output_server[8], packed_output_local[8];

    char inp[17], out[17];

    input_file.open(input_file_name);
    output_file.open(output_file_name);

    while (input_file >> inp) {
        if_correct = true;
        output_file >> out;

        packed8_from_sp_hex(inp, packed_input);
        packed8_from_sp_hex(out, packed_output_server);

        des(packed_input, packed_output_local, 6, 'N');

        for(INT i = 0; i < 8; ++i) {
            if (packed_output_local[i] != packed_output_server[i])
                if_correct = false;
            cout << (int)packed_output_local[i] << ' ';
        }
        cout << endl;
        for(INT i = 0; i < 8; ++i) {
            cout << (int)packed_output_server[i] << ' ';
        }
        cout << endl;

        if (if_correct) ctr++;
    }

    input_file.close();
    output_file.close();

    return ctr;
}

void recurse(char *key, int start) {
    while (start < 64) {
        if (key[start] != 'x') ++start;
        else break;
    }
    if (start == 64) {
        int tmp = check_key(key);
        if (tmp)
           cout << key << ": " << tmp << '\n';
    } else {
        key[start] = '0';
        recurse(key, start+1);
        key[start] = '1';
        recurse(key, start+1);
        key[start] = 'x';
    }
}

int main(int argc, char **argv) {
    if (argc != 4) {
        print_format(argv[0]);
        return 0;
    }
    input_file_name = argv[1];
    output_file_name = argv[2];

    recurse(argv[3], 0);

    return 0;
}
