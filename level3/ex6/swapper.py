def transposeMatrix(m):
    """ Transpose a square matrix """
    t = []
    dim = range(len(m))
    for i in dim:
        tRow = []
        for j in dim:
            tRow.append(m[j][i])
        t.append(tRow)
    return t

def multiplyVectors(v,j):
    """Return the dot product of 2 vectores of same dim."""
    if len(v) != len(j):
        raise Exception("Cannot multiply vectors of incompatible size")
    dp = 0
    for x,y in zip(v,j):
        dp += x*y
    return dp
    
def multiply(a, b):
    """Return the product of 2 square matrices of same dim."""
    if a == [] or b == []:
        raise Exception("Cannot multiply empty matrices")

    if len(a[0]) != len(b):
        raise Exception("Cannot multiply matrices of incompatible sizes")

    m = []
    transB = transposeMatrix(b)
    for l in transB:
        print l
    dim = len(a)
    
    for i in range(dim):
        mRow = []
        for j in range(dim):
            print a[i], transB[j]
            mRow.append(multiplyVectors(a[i], transB[j]))
        m.append(mRow)
    return m

v = [1,2,8]
j = [3,0,9]
f = [4, 2+3, 3+3]


A = [v,j,f]

print(multiply(A,A))