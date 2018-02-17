#include <iostream>
#include <fstream>
#include <cstdlib>
#include <map>
#include <vector>
#include "des.cc"
using namespace std;

ifstream input_pair_file, output_pair_file;
unsigned long long tobenum = 67108864;

void print_format(char *binary_exec_str) {
    cout << "Usage:" << endl;
    cout << binary_exec_str << " <File with input pairs> \n\
        <File with corresponding output pairs> \n\
        <binary mask for choosing S boxes> \n\
        <c': value to xor with l'>" << endl;
}

void print_array(BYTE *arr, int len) {
    for(INT i = 0; i < len; ++ i) {
        cout << (int)arr[i];
        if ((i & 0x3) == 0x3) cout << ' ';
    }

    cout << endl;
}

bool SBOX_MAP[8];

int main(int argc, char **argv) {
    if (argc != 5) {
        print_format(argv[0]);
        return 0;
    }

    for(int i=0;i<8;i++)
        if(argv[3][i] == '1')
            SBOX_MAP[i] = true;
        else
            SBOX_MAP[i] = false;

    // input_pair_file.open(argv[1]);
    output_pair_file.open(argv[2]);

    // Get bits from the keys
    // Input c is in hex and has to be converted to bit representation
    BYTE packed_c_diff[8], unpacked_c_diff[64];
    if (get_packed8_from_hex(argv[4], packed_c_diff) < 0) {
        print_format(argv[0]);
        return 0;
    }
    unpack8(packed_c_diff, unpacked_c_diff);

    // c unpacked to bit representation
    // cout << "c': input to last round as L\n";
    // print_array(unpacked_c_diff, 32);

    // Stores the output ciphers (Lo,Ro), (Lo*, Ro*)
    char output_str[2][256];

    BYTE output_packed[2][8], output_unpacked[2][64];
    BYTE unpermuted_output_unpacked[2][64];
    BYTE cipher_diff[64], unpermuted_op_diff[64];
    BYTE *fbox_ip[2];
    BYTE fbox_op_diff[32];

    INT key_ctr[8][64] = {};

    // For each output pair in the input file convert it
    // to the binary representation and then perform our check for the key
    while(output_pair_file >> output_str[0]) {
        output_pair_file >> output_str[1];

        // ********************
        // Handling the outputs
        // ********************

        for(INT i = 0; i < 2; ++ i) {
            packed8_from_sp_hex(output_str[i], output_packed[i]);
            unpack8(output_packed[i], output_unpacked[i]);
        }

        // Perform the "inverse of RFP" to get the output of DES
        // before performing RFP
        for(INT i = 0; i < 64; ++ i) {
            unpermuted_output_unpacked[0][i] = output_unpacked[0][RFP_INV[i]-1];
            unpermuted_output_unpacked[1][i] = output_unpacked[1][RFP_INV[i]-1];
        }

        // Outputs unpacked to bit representation
        // cout << "Output unpacked:\n";
        // print_array(output_unpacked[0], 64);

        // cout << "Output* unpaked:\n";
        // print_array(output_unpacked[1], 64);

        // Calculate the output differential and store in cipher_diff
        // unsigned long long num = 0;
        for(INT i = 0; i < 64; ++ i) {
            cipher_diff[i] = unpermuted_output_unpacked[0][i] ^ unpermuted_output_unpacked[1][i];
            // if(i<32)
            //     num = (num<<1) + cipher_diff[i];
        }
        // cout<<num<<endl;
        // if(num != tobenum) continue;

        //cout << "Output diff permuted:\n";
        //print_array(cipher_diff, 64);

        //cout << "Output diff unpermuted:\n";
        //print_array(unpermuted_op_diff, 64);

        // 1) XOR the output differential of the DES and c'
        // to get the output differential of the S boxes in the last round
        // 2) Reverse the inverse of the P boxes
        // The last 32 bits of the output are the output of the last round
        // Doubt
        for(INT i = 0; i < 32; ++ i) {
            fbox_op_diff[i] = cipher_diff[INV_P[i]-1+32] ^
                unpacked_c_diff[INV_P[i]-1];
        }

        // ********************
        // Handling the inputs
        // ********************

        // Get Lo, Lo* from the input
        // These are the inputs for the last round encryption function
        // fbox_ip_diff = &(unpermuted_op_diff[32]);
        //
        // The first 32 bits of output are the R in the last round
        fbox_ip[0] = &(unpermuted_output_unpacked[0][0]);
        fbox_ip[1] = &(unpermuted_output_unpacked[1][0]);

        vector<long long> keynums[8];

        for(INT t = 0; t < 8; ++ t) {
            if (argv[3][t] == '1') {
                BYTE expanded_ip[2] = {0, 0}, sbox_ip[2] = {};
                for(INT k = 0; k < 2; ++ k)
                    for(INT i = 0; i < 6; ++ i) {
                        expanded_ip[k] <<= 1;
                        expanded_ip[k] += fbox_ip[k][E[6*t + i]-1];
                    }
                // cout<<"The expanded_ip1 is "<<(int)expanded_ip[0]<<endl;
                // cout<<"The expanded_ip2 is "<<(int)expanded_ip[1]<<endl;

                BYTE sbox_op_diff = 0;
                for(INT i = 0; i < 4; ++i)
                    sbox_op_diff = (sbox_op_diff<<1) + fbox_op_diff[(t<<2)+i];
                // cout<<"The sbox_op_diff is "<<(int)sbox_op_diff<<endl;

                for(BYTE key = 0; key < 64; ++ key) {
                    sbox_ip[0] = key ^ expanded_ip[0];
                    sbox_ip[1] = key ^ expanded_ip[1];

                    if (sbox_op_diff == (S[t][S_MAP[sbox_ip[0]]-1] ^
                                S[t][S_MAP[sbox_ip[1]]-1])) {
                        keynums[t].push_back(key);
                        ++ key_ctr[t][key];
                    }
                }
            }
        }
    }

    for (INT t = 0; t < 8; ++ t) {
        if (argv[3][t] == '1') {
            cout << t << ": " << endl;
            for(INT i = 0; i < 64; ++ i)
                cout << i << ":" << key_ctr[t][i] << ' ';
            cout << endl;
        }
    }

    return 0;
}

