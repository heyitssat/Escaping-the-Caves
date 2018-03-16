#include <iostream>
#include <fstream>
using namespace std;

typedef unsigned char BYTE;
typedef unsigned int CTR;

const BYTE BLOCK_WIDTH = 7;
const BYTE NUM_BLOCKS = 8;
const BYTE NUM_INPUTS_PER_LINE = 1<<BLOCK_WIDTH;

ofstream OutFile;

char sp_hex_map[] = {'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u'};

void print_format(char *binary_exec_str) {
    cout << "Usage:" << endl;
    cout << binary_exec_str << " <output-file>\n\
        <number of output plaintexts>" << endl;
}

void print_array(BYTE* a, int len) {
    for(int i=0;i<len;i++){
        cout<<(int)a[i]<<" ";
    }
    cout<<endl;
}

int main(int argc, char **argv) {

    if (argc != 3) {
        print_format(argv[0]);
        return 0;
    }

    OutFile.open(argv[1]);
    CTR line_count = atoi(argv[2]);

    BYTE input_text[NUM_BLOCKS];
    for (CTR i = 0; i < line_count; ++i) {
        CTR block_to_permute = i % NUM_BLOCKS;
        CTR constant_value = i / NUM_BLOCKS;

        for (CTR k = 0; k < NUM_BLOCKS; ++ k)
            input_text[k] = constant_value;

        for (CTR j = 0; j < NUM_INPUTS_PER_LINE; ++ j) {
            input_text[block_to_permute] = j;

            for (CTR k = 0; k < NUM_BLOCKS; ++ k)
                OutFile << sp_hex_map[input_text[k] >> 4] <<
                    sp_hex_map[input_text[k] & 0xf];

            if (j == NUM_INPUTS_PER_LINE-1) OutFile << '\n';
            else OutFile << ' ';
        }

    }

    OutFile.close();

    return 0;
}
