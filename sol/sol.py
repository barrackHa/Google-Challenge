# Given Absorbing Markov Chain find Absorbing Probabilities
# From Wikipedia: https://en.wikipedia.org/wiki/Absorbing_Markov_chain
#
# AMC is represented in a form:
# [Q R]
# [O I]
# where Q - t-by-t matrix of probabilities of transition between transient states,
# R - t-by-r matrix of probabilities of transition from transient to absorbing states,
# O - zero matrix
# I - identity matrix (in our particular case we're provided with zero matrix)
#
# Absorbing Probabilities are determined as:
# B = (I - Q)^-1 * R

from fractions import Fraction

def transientsCount(m):
    """
        Take m - a sorted square matrix under the conditions of
        the assignment and return the number of transients states.
        assume absorbing states follow transient states w/o interlieveing.
    """
    dim = len(m)
    r = 0
    # Assuming it is guaranteed that no matter which state the ore is in,
    # there is a path from that state to a terminal state.
    while (r < dim and sum(m[r]) != 0):
        r += 1
    return r

def decompose(m):
    """
        decompose input matrix m on Q (t-by-t) and R (t-by-r) components.
        t is the number of transient states. r = dim(m) - t.
    """
    t = transientsCount(m)
    Q = []
    R = []
    for r in range(t):
        Q.append(m[r][:t])
        R.append(m[r][t:])
    return Q, R

def identity(t):
    """Create a t by t identity matrix."""
    m = []
    for i in range(t):
        r = [int(i == j) for j in range(t)]
        m.append(r)
    return m

def isZero(m):
    """Return True IFF m is the zero matrix."""
    row_summed = [sum(r) for r in m] 
    return sum(row_summed) == 0

def swap(m, i, j):
    """ Swap i,j rows/columns of a square matrix m."""
    if i == j:
        # no need to swap
        return m
    # swap column space
    for r in m:
        r[i], r[j] = r[j], r[i]
    # swap row space
    m[i], m[j] = m[j], m[i]
    return m

def sort(m):
    """
        reorganize matrix so zero-rows go last 
        (preserving zero rows order)
    """
    size = len(m)

    zero_row = -1
    for r in range(size):
        r_sum =sum(m[r])
        if r_sum == 0:
            # we have found all-zero row, remember it
            zero_row = r
        if r_sum != 0 and zero_row > -1:
            # we have found non-zero row after all-zero row - swap these rows
            n = swap(m, r, zero_row)
            # and repeat from the begining
            return sort(n)
    #nothing to sort, return
    return m

def normalize(m):
    """ Normalize matrix m """
    n = []
    for row in m:
        nRow = []
        denom = sum(row) 
        if denom == 0:
            # all-zero row
            nRow = row
        else:
            nRow = [Fraction(num, denom) for num in row]
        n.append(nRow)
    return n

def subtract(i, q):
    """ Subtract two square matrices with equal dims."""
    if len(i) != len(i[0]) or len(q) != len(q[0]):
        raise Exception("non-square matrices")

    if len(i) != len(q):
        raise Exception("Cannot subtract matrices of different sizes")

    s = []
    d = len(i) 
    for r in range(d):
        sRow = []
        for c in range(d):
            sRow.append(i[r][c] - q[r][c])
        s.append(sRow)
    return s

def transposeMatrix(m):
    """ Transpose matrix """
    t = []
    for i in range(len(m)):
        tRow = []
        for j in range(len(m[0])):
            tRow.append(m[j][i])
        t.append(tRow)
    return t

def multiply(a, b):
    """Return the product of 2 matrices of incompatible dims."""
    if a == [] or b == []:
        raise Exception("Cannot multiply empty matrices")

    if len(a[0]) != len(b):
        raise Exception("Cannot multiply matrices of incompatible sizes")

    m = []
    rows = len(a)
    cols = len(b[0])
    iters = len(a[0])

    for r in range(rows):
        mRow = []
        for c in range(cols):
            dotProd = 0
            for i in range(iters):
                dotProd += a[r][i]*b[i][c]
            mRow.append(dotProd)
        m.append(mRow)
    return m

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    """Return matrix determinant using Laplace expansion."""
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    d = 0
    for c in range(len(m)):
        d += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))

    return d

def getMatrixInverse(m):
    """
        Return matrix invers for inversable matrix m.
        m^(-1) = (det(m))^(-1) * adj(m)
    """
    d = getMatrixDeternminant(m)

    if d == 0:
        raise Exception("Cannot get inverse of matrix with zero determinant")

    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/d, -1*m[0][1]/d],
                [-1*m[1][0]/d, m[0][0]/d]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/d
    return cofactors

def calculateB(m):
    """ 
        return B = (I-Q)^-1 * R = V*R 
        A limiting absorbing Markov transition matrix.
    """
    m = sort(m)
    n = normalize(m)
    (q, r) = decompose(n)
    i = identity(len(q))
    s = subtract(i, q)
    v = getMatrixInverse(s)
    b = multiply(v, r)
    return b

def gcd(a, b):  
    """Euclid's algorithm for greatest common divisor"""
    if a == 0 : 
        return b  
    return gcd(b%a, a) 

def lcm(a, b):
    """Return least common multiple of two int's"""
    return (a*b)/gcd(a,b)
    
def lcmOfList(l):
    return reduce(lambda x, y: lcm(x, y), l)

def listTermStates(probs):
    """
        The matrix B = (I - Q)^-1 * R is the limit of the Absorbing Markov Chain
        transition matrix. It's first row gives the probs arg as a list of
        Fraction instanses. returns an array of ints for each terminal state 
        giving the exact probabilities of each terminal state, 
        represented as the numerator for each state, 
        then the denominator for all of them at the end and in simplest form. 
    """
    probsLcm = lcmOfList([f.denominator for f in probs])
    termStates = [
        (probsLcm / f.denominator) * f.numerator
        for f in probs    
    ]
    termStates.append(probsLcm)    
    return termStates

def solution(m):
    if len(m) == 1:
        return [1,1]
    probs = calculateB(m)[0]
    return listTermStates(probs)


# m = [
#     [0, 2, 1, 0, 0], 
#     [0, 0, 0, 3, 4], 
#     [0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0]
# ]

# print(swap(m,0,1))
