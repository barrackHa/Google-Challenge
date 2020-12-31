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


# get number of transients states
# assume absorbing states follow transient states w/o interlieveing
from fractions import Fraction

def num_of_transients(m):
    """
        Take m - a sorted square matrix under the conditions of
        the assignment and return the number of zero - rows 
    """
    dim = len(m)
    r = 0
    while (r < dim and sum(m[r]) != 0):
        r += 1
    return r

# decompose input matrix `m` on Q (t-by-t) and R (t-by-r) components
# `t` is the number of transient states
def decompose(m):
    t = num_of_transients(m)
    if t == 0:
        raise Exception("No transient states. At least initial state is needed.")

    Q = []
    for r in range(t):
        qRow = []
        for c in range(t):
            qRow.append(m[r][c])
        Q.append(qRow)
    if Q == []:
        raise Exception("Not a valid AMC matrix: no transient states")

    R = []
    for r in range(t):
        rRow = []
        for c in range(t, len(m[r])):
            rRow.append(m[r][c])
        R.append(rRow)
    if R == []:
        raise Exception("Not a valid AMC matrix: missing absorbing states")
    return Q, R

# return Identity matrix of size `t`
def identity(t):
    m = []
    for i in range(t):
        r = []
        for j in range(t):
            r.append(int(i == j))
        m.append(r)
    return m

# check if the matrix is zero
def isZero(m):
    row_summed = [sum(r) for r in m] 
    return sum(row_summed) == 0 


# swap i,j rows/columns of a square matrix `m`
def swap(m, i, j):
    n = []
    s = len(m)

    if i == j:
        # no need to swap
        return m

    for r in range(s):
        nRow = []
        tmpRow = m[r]
        if r == i:
            tmpRow = m[j]
        if r == j:
            tmpRow = m[i]
        for c in range(s):
            tmpEl = tmpRow[c]
            if c == i:
                tmpEl = tmpRow[j]
            if c == j:
                tmpEl = tmpRow[i]
            nRow.append(tmpEl)
        n.append(nRow)
    return n

# reorganize matrix so zero-rows go last (preserving zero rows order)
def sort(m):
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

# normalize matrix `m`
def normalize(m):
    n = []
    for row in m:
        nRow = []
        denom = sum(row) 
        if denom == 0:
            # all-zero row
            nRow = row
        else:
            for num in row:
                nRow.append(Fraction(num, denom))
        n.append(nRow)
    return n

# subtract two matrices
def subtract(i, q):
    if len(i) != len(i[0]) or len(q) != len(q[0]):
        raise Exception("non-square matrices")

    if len(i) != len(q) or len(i[0]) != len(q[0]):
        raise Exception("Cannot subtract matrices of different sizes")

    s = []
    for r in range(len(i)):
        sRow = []
        for c in range(len(i[r])):
            sRow.append(i[r][c] - q[r][c])
        s.append(sRow)
    return s

# multiply two matrices
def multiply(a, b):
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
            sum = 0
            for i in range(iters):
                sum += a[r][i]*b[i][c]
            mRow.append(sum)
        m.append(mRow)
    return m

# transpose matrix
def transposeMatrix(m):
    t = []
    for r in range(len(m)):
        tRow = []
        for c in range(len(m[r])):
            if c == r:
                tRow.append(m[r][c])
            else:
                tRow.append(m[c][r])
        t.append(tRow)
    return t

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

# matrix determinant
def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    d = 0
    for c in range(len(m)):
        d += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))

    return d

# matrix inversion
def getMatrixInverse(m):
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

def calculate_b(m):
        # B = (I-Q)^-1 * R
        m = sort(m)
        n = normalize(m)
        (q, r) = decompose(n)
        i = identity(len(q))
        s = subtract(i, q)
        v = getMatrixInverse(s)
        b = multiply(v, r)
        return b

def lcm(a, b):
    if a > b:
        greater = a
    else:
        greater = b

    while True:
        if greater % a == 0 and greater % b == 0:
            lcm = greater
            break
        greater += 1

    return lcm


def get_lcm_for(l):
    return reduce(lambda x, y: lcm(x, y), l)

def convert_to_lcd(probs):
    ret = []
    least_common_multiple = get_lcm_for([f.denominator for f in probs])
    for f in probs:
        if f.denominator != least_common_multiple:
            ret.append(
                least_common_multiple / f.denominator * f.numerator
            )
        else:
            ret.append(f.numerator)
    ret.append(least_common_multiple)    
    return ret

def solution(m):
    if len(m) == 1:
        return [1,1]
    probs = calculate_b(m)[0]
    return convert_to_lcd(probs)




# m = [
#     [0, 2, 1, 0, 0], 
#     [0, 0, 0, 3, 4], 
#     [0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0]
# ]

# print(swap(m,0,1))
