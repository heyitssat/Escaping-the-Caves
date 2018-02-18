from utility import *
import sys

input_file = sys.argv[1]

def check_duplicates(line):
    s = set()
    parts = [line[i:i+16] for i in range(0, len(line), 16)]
    uniq_parts = [p for p in parts if p not in s and not s.add(p)]
    if (len(uniq_parts) == len(parts)):
        return False
    else:
        print("The duplication amount is {}".format(len(parts) - len(uniq_parts)))
        return True

with open(input_file, 'r') as f:
    lines = f.readlines()
    count = 0
    for line in lines:
        if check_duplicates(line):
            count += 1
            print(line)

print(count)
