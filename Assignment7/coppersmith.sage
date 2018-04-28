import time

debug = False

# display matrix picture with 0 and X
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii,jj] == 0 else 'X'
            a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        print a

def coppersmith_howgrave_univariate(pol, modulus, beta, mm, tt, XX):
    """
    Coppersmith revisited by Howgrave-Graham

    finds a solution if:
    * b|modulus, b >= modulus^beta , 0 < beta <= 1
    * |x| < XX
    """
    #
    # init
    #
    dd = pol.degree()
    nn = dd * mm + tt

    #
    # checks
    #
    if not 0 < beta <= 1:
        raise ValueError("beta should belongs in (0, 1]")

    if not pol.is_monic():
        raise ArithmeticError("Polynomial must be monic.")

    #
    # calculate bounds and display them
    #
    """
    * we want to find g(x) such that ||g(xX)|| <= b^m / sqrt(n)

    * we know LLL will give us a short vector v such that:
    ||v|| <= 2^((n - 1)/4) * det(L)^(1/n)

    * we will use that vector as a coefficient vector for our g(x)

    * so we want to satisfy:
    2^((n - 1)/4) * det(L)^(1/n) < N^(beta*m) / sqrt(n)

    so we can obtain ||v|| < N^(beta*m) / sqrt(n) <= b^m / sqrt(n)
    (it's important to use N because we might not know b)
    """
    if debug:
        # t optimized?
        print "\n# Optimized t?\n"
        print "we want X^(n-1) < N^(beta*m) so that each vector is helpful"
        cond1 = RR(XX^(nn-1))
        print "* X^(n-1) = ", cond1
        cond2 = pow(modulus, beta*mm)
        print "* N^(beta*m) = ", cond2
        print "* X^(n-1) < N^(beta*m) \n-> GOOD" if cond1 < cond2 else "* X^(n-1) >= N^(beta*m) \n-> NOT GOOD"

        # bound for X
        print "\n# X bound respected?\n"
        print "we want X <= N^(((2*beta*m)/(n-1)) - ((delta*m*(m+1))/(n*(n-1)))) / 2 = M"
        print "* X =", XX
        cond2 = RR(modulus^(((2*beta*mm)/(nn-1)) - ((dd*mm*(mm+1))/(nn*(nn-1)))) / 2)
        print "* M =", cond2
        print "* X <= M \n-> GOOD" if XX <= cond2 else "* X > M \n-> NOT GOOD"

        # solution possible?
        print "\n# Solutions possible?\n"
        detL = RR(modulus^(dd * mm * (mm + 1) / 2) * XX^(nn * (nn - 1) / 2))
        print "we can find a solution if 2^((n - 1)/4) * det(L)^(1/n) < N^(beta*m) / sqrt(n)"
        cond1 = RR(2^((nn - 1)/4) * detL^(1/nn))
        print "* 2^((n - 1)/4) * det(L)^(1/n) = ", cond1
        cond2 = RR(modulus^(beta*mm) / sqrt(nn))
        print "* N^(beta*m) / sqrt(n) = ", cond2
        print "* 2^((n - 1)/4) * det(L)^(1/n) < N^(beta*m) / sqrt(n) \n-> SOLUTION WILL BE FOUND" if cond1 < cond2 else "* 2^((n - 1)/4) * det(L)^(1/n) >= N^(beta*m) / sqroot(n) \n-> NO SOLUTIONS MIGHT BE FOUND (but we never know)"

        # warning about X
        print "\n# Note that no solutions will be found _for sure_ if you don't respect:\n* |root| < X \n* b >= modulus^beta\n"

    #
    # Coppersmith revisited algo for univariate
    #

    # change ring of pol and x
    polZ = pol.change_ring(ZZ)
    x = polZ.parent().gen()

    # compute polynomials
    gg = []
    for ii in range(mm):
        for jj in range(dd):
            gg.append((x * XX)**jj * modulus**(mm - ii) * polZ(x * XX)**ii)
    for ii in range(tt):
        gg.append((x * XX)**ii * polZ(x * XX)**mm)

    # construct lattice B
    BB = Matrix(ZZ, nn)

    for ii in range(nn):
        for jj in range(ii+1):
            BB[ii, jj] = gg[ii][jj]

    # display basis matrix
    if debug:
        matrix_overview(BB, modulus^mm)

    # LLL
    BB = BB.LLL()

    # transform shortest vector in polynomial
    new_pol = 0
    for ii in range(nn):
        new_pol += x**ii * BB[0, ii] / XX**ii

    # factor polynomial
    potential_roots = new_pol.roots()
    if debug:
        print "potential roots:", potential_roots

    # test roots
    roots = []
    for root in potential_roots:
        if root[0].is_integer():
            result = polZ(ZZ(root[0]))
            if gcd(modulus, result) >= modulus^beta:
                roots.append(ZZ(root[0]))

    #
    return roots

############################################
# Test on Stereotyped Messages
##########################################

e = 5
N = 76532186921483925730333542860471947569801645804927004439844851550880096311592576593105686443799049446797577841173822698646267313417166086664815894345719921973323809838945385603976950397294860842646798263077572800433554840518978151675036652812391378489590219684082031027638892138605077068151604517037533012009
C = 15678940324561979146526999262590873357560603336055698666940209207194948566254184765405829874917109010191410262945843468417965580953024119634541231188624432761799031307951858315989766145110379494566289550479562190203669289344966044545989710068668160971462095110923039715928073506290280724752848180050539166557

# RSA known parameters
ZmodN = Zmod(N);

def break_RSA(M_str, max_length_x):
    global e, C, ZmodN

    print len(M_str), ' ' + M_str
    M_binary_str = ''.join(['{0:08b}'.format(ord(x)) for x in M_str])
    print(int(M_binary_str, 2))

    # M_binary_rev = list(M_binary_str)
    # M_binary_rev.reverse()

    # Mx = ZZ([1]*24 + M_binary_rev, 2)
    # # print('{0:b}'.format(Mx))
    # # print(M_binary_str)
    # C = ZmodN(Mx)^e
    # print('C: ',C)

    for length_x in range(0, max_length_x+1, 4):          # size of the root

        # Problem to equation (default)
        P.<x> = PolynomialRing(ZmodN) #, implementation='NTL')
        pol = ((int(M_binary_str, 2)<<length_x) + x)^e - C
        dd = pol.degree()

        # Tweak those
        beta = 1                                # b = N
        epsilon = beta / 7                      # <= beta / 7
        mm = ceil(beta**2 / (dd * epsilon))     # optimized value
        tt = floor(dd * mm * ((1/beta) - 1))    # optimized value
        XX = ceil(N**((beta**2/dd) - epsilon))  # optimized value

        # Coppersmith
        # start_time = time.time()
        roots = coppersmith_howgrave_univariate(pol, N, beta, mm, tt, XX)

        # output
        if roots:
            print "\n# Solutions @", length_x
            # print "we want to find:",str(K)
            print "we found:", ' {0:b}'.format(roots[0])
            # print("in: %s seconds " % (time.time() - start_time))
            print "\n"
            return

    print 'No solution found\n'

if __name__ == "__main__":
    with open('paddings.txt','r') as f:
        M_list = f.readlines()

    for M in M_list:
        break_RSA(M.strip(), 300)
