from fractions import Fraction

def copy(arr2d):
    """returns a deep copy of a 2d array"""
    assert(arr2d[0])
    m = [l[:] for l in arr2d]
    return m

class Matrix():
    def __init__(self, m):
        self.mat = copy(m)
        self.rowDim = len(m)
        self.colDim = len(m[0])
        return

    def __str__(self):
        s = ''
        for l in self.mat:
            s += str(l) + '\n'
        return s

    def __getitem__(self, i): 
        """Getter for the matrix I'th row"""  
        return self.mat[i]
    
    def __setitem__(self, i, row): 
        """Setter for the matrix I'th row""" 
        if len(row) != self.colDim:
            raise Exception("Row vector dim must be equal to Matrix's column dim")
        self.mat[i] = row[:]
        return self

    def __iter__(self):
        for l in self.mat:
            yield l

    @property
    def isSquare(self):
        return self.colDim == self.rowDim

    @property
    def isZero(self):
        """Return True IFF m is the zero matrix."""
        row_summed = [sum(r) for r in self] 
        return sum(row_summed) == 0


    def transposeMatrix(self):
        """ Return a new instance of Transpose matrix """
        t = []
        for i in range(len(m)):
            tRow = []
            for j in range(len(m[0])):
                tRow.append(m[j][i])
            t.append(tRow)
        return Matrix(t)
    
    def getMatrixMinor(self,i,j):
        """
            A new matrix inst made of the old matrix by deleting the
            I'th row and J'th column. 
        """
        return Matrix(
            [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]
        )
    
    def getMatrixDeternminant(self):
        """Return matrix determinant using Laplace expansion."""
        #base case for 2x2 matrix
        m = copy(self.mat)
        if self.rowDim == 2:
            return m[0][0]*m[1][1]-m[0][1]*m[1][0]
        #Continue recursively on the minors
        d = 0
        for c in range(self.rowDim):
            d += ((-1)**c)*m[0][c]*self.getMatrixMinor(0,c)\
                                       .getMatrixDeternminant()
        return d

    def getMatrixInverse(self):
        """
            Return matrix invers for inversable matrix m.
            m^(-1) = (det(m))^(-1) * adj(m)
        """
        d = self.getMatrixDeternminant()
        m = copy(self.mat)

        if d == 0:
            raise Exception("Cannot get inverse of matrix with zero determinant")

        #special case for 2x2 matrix:
        if self.rowDim == 2:
            return Matrix([
                [m[1][1]/d, -1*m[0][1]/d],
                [-1*m[1][0]/d, m[0][0]/d]
            ])

        #find matrix of cofactors AKA adj(m)
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(r,c)
                cofactorRow.append(
                    ((-1)**(r+c)) * minor.getMatrixDeternminant()
                )
            cofactors.append(cofactorRow)
        cofactors = Matrix(cofactors).transposeMatrix()
        
        # Divide adj by the determinant
        for r in range(cofactors.rowDim):
            for c in range(cofactors.colDim):
                cofactors[r][c] = cofactors[r][c]/d
        return Matrix(cofactors)

    def multiply(self, other):
        """Return the product of 2 matrices of incompatible dims."""
        if self.mat == [] or other.mat == []:
            raise Exception("Cannot multiply empty matrices")

        if self.colDim != other.rowDim :
            raise Exception("Cannot multiply matrices of incompatible sizes")

        m = []
        rows = self.rowDim
        cols = other.colDim
        iters = self.colDim

        for r in range(rows):
            mRow = []
            for c in range(cols):
                dotProd = 0
                for i in range(iters):
                    dotProd += self[r][i] * other[i][c]
                mRow.append(dotProd)
            m.append(mRow)
        return Matrix(m)

    def subtract(self, other):
        """ Subtract two square matrices with equal dims."""
        if (not self.isSquare) or (not other.isSquare):
            raise Exception("non-square matrices")

        if self.rowDim != other.rowDim:
            raise Exception("Cannot subtract matrices of different sizes")

        s = []
        d = self.rowDim 
        for r in range(d):
            sRow = []
            for c in range(d):
                sRow.append(self[r][c] - other[r][c])
            s.append(sRow)
        return Matrix(s)

    def swap(self, i, j):
        """ Swap i,j rows/columns of a square matrix m."""
        if i == j:
            # no need to swap
            return self
        # swap column space
        for r in self:
            r[i], r[j] = r[j], r[i]
        # swap row space
        self[i], self[j] = self[j], self[i]
        return self

    @classmethod
    def identity(cls, d):
        """Create a d by d identity matrix."""
        m = []
        for i in range(d):
            r = [int(i == j) for j in range(d)]
            m.append(r)
        return Matrix(m)

class AMC(Matrix):
    """
        Given Absorbing Markov Chain (AMC) find Absorbing Probabilities
        From Wikipedia: https://en.wikipedia.org/wiki/Absorbing_Markov_chain

        AMC is represented in a form:
        [Q R]
        [O I]
        where Q - t-by-t matrix of probabilities of transition between transient states,
        R - t-by-r matrix of probabilities of transition from transient to absorbing states,
        O - zero matrix
        I - identity matrix (in our particular case we're provided with zero matrix)

        Absorbing Probabilities are determined as:
        B = (I - Q)^-1 * R
    """

    def __init__(self, m):
        Matrix.__init__(self, m)
        return

    def sort(self):
        """
            reorganize matrix so zero-rows go last 
            (preserving zero rows order)
        """
        zero_row = -1
        for r in range(self.rowDim):
            r_sum =sum(self[r])
            if r_sum == 0:
                # we have found all-zero row, remember it
                zero_row = r
            if r_sum != 0 and zero_row > -1:
                # we have found non-zero row after all-zero row - swap these rows 
                # and repeat from the begining
                return self.swap(r, zero_row).sort()
        #nothing to sort, return
        return self

    def transientsCount(self):
        """
            Take m - a sorted square matrix under the conditions of
            the assignment and return the number of transients states.
            Assuming it is guaranteed that no matter which state the ore is in,
            there is a path from that state to a terminal state.    
        """
        r = 0
        while (r < self.rowDim and sum(self[r]) != 0):
            r += 1
        return r

    def decompose(self):
        """
            decompose matrix on Q (t-by-t) and R (t-by-r) components.
            t is the number of transient states. r = dim(matrix) - t.
        """
        t = self.transientsCount()
        Q = []
        R = []
        for r in range(t):
            Q.append(self[r][:t])
            R.append(self[r][t:])
        return Matrix(Q), Matrix(R)

    def normalize(self):
        """ Normalize matrix """
        n = []
        for row in self:
            nRow = []
            denom = sum(row) 
            if denom == 0:
                # all-zero row
                nRow = row
            else:
                nRow = [Fraction(num, denom) for num in row]
            n.append(nRow)
        return AMC(n)

    def calculateB(self):
        """ 
            return B = (I-Q)^-1 * R = V*R 
            A limiting absorbing Markov transition matrix.
        """
        self.sort()
        N = self.normalize()
        Q, R = N.decompose()
        I = Matrix.identity(Q.rowDim)
        S = I.subtract(Q)
        V = S.getMatrixInverse()
        B = V.multiply(R)
        return B


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
    probs = AMC(m).calculateB()[0]
    return listTermStates(probs)



# m = [[0.3,0.7],[0,0]]
# M = AMC(m)
# print M.swap(0,1)
# print(M.sort())
# print M.transientsCount()
# Q, R = M.decompose()
# print Q, " R -  ", R

A = AMC([
    [0, 2, 1, 0, 0], 
    [0, 0, 0, 3, 4], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0]
])
# print A.normalize()
# print A.calculateB()

mmm = [
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]

print solution(mmm) 

print solution([
    [0, 2, 1, 0, 0], 
    [0, 0, 0, 3, 4], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0]
]) == [7, 6, 8, 21]

print solution([
    [0, 1, 0, 0, 0, 1], 
    [4, 0, 0, 3, 2, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0]
]) == [0, 3, 2, 9, 14]


# m = [[0,0,1],[0,1,0],[1,0,0]]
# M = Matrix(m)
# print M
# print M.transposeMatrix()
# print M.getMatrixMinor(1,0)
# print M.getMatrixDeternminant()
# print M.getMatrixInverse()
# print M.subtract(M)
# M2 = Matrix([[1,2],[3,4]])
# print M2.swap(0,1)
# print M2.isZero
# z = M.subtract(M)
# print z.isZero
# print Matrix.identity(3)


# m = [
#     [0, 2, 1, 0, 0], 
#     [0, 0, 0, 3, 4], 
#     [0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0]
# ]

# print(swap(m,0,1))


