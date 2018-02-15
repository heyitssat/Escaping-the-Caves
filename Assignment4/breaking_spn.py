
def break_sbox(sbox):
    size_sbox = len(sbox)

    def getno(n):
        c = 0
        while(n):
            if(n%2==1):
                c+=1
            n=int(n/2)
        return c

    def bias(inp_mask, out_mask):
        count = 0
        for (inp, outp) in enumerate(sbox):
            if ((getno(inp & inp_mask) + getno(outp & out_mask)) % 2 == 0):
                count += 1
        return count

    def pairs(size):
        return [(im, om) for im in range(size) for om in range(size)]

    counts = {
            (im, om) : bias(im, om) for (im, om) in pairs(size_sbox)
            }
    return counts

def pretty_print(d, size):
    l = ["x\y"] + [i for i in range(size)]
    print(*l, sep="\t")
    for n in range(size):
        l = [n] + [c for m, c in d.items() if m[0]==n]
        print(*l, sep="\t")
    #  print("\t" + str(k) + ":\t" + str(v))

sbox = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]

pretty_print(break_sbox(sbox), len(sbox))

def getno(n):
    c = 0
    while(n):
        if(n%2==1):
            c+=1
        n=int(n/2)
    return c

def bias(inp_mask, out_mask, sbox):
    count = 0
    for (inp, outp) in enumerate(sbox):
        if ((getno(inp & inp_mask) + getno(outp & out_mask)) % 2 == 0):
            count += 1
            #  print(str(inp & inp_mask) +"\t"+str(outp & out_mask))
            #  print(str(inp) + "\t" + str(outp))
            #  print(str(getno(inp & inp_mask)) +"\t"+str(getno(outp & out_mask)))
    return count

print(bias(3, 9, sbox))
