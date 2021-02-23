from math import sqrt, floor, pow

sqrt2 = sqrt(2)
# print floor(sqrt2)
def tester(str_n):
    n = float(str_n)
    tot, i = 0, 1
    while i <= n:
        tot += float(floor((i)*sqrt2))
        assert floor((i)*sqrt2) == (i*sqrt2) - ((i*sqrt2)%1)
        i += 1
    return tot

def beattySum(coef, upperBounb):
    beattySeq = lambda x: floor(coef * x)
    tot, i = 0, 1
    beaty = beattySeq(i)
    while beaty <= upperBounb:
        tot += beaty
        i += 1
        beaty = beattySeq(i)
    return tot

def solution(str_n):
    """
    1/alph + 1/beta = 1
    1/beta = 1 - 1/alpha ( != 0 )
    beta = 1 / (1 - 1/alpha)
    m = floor(n * alpha)
    sum([1,...,m]) = beattySum(alpha, n) + beattySum(beta, floor(m/beta))
    ergo:
    beattySum(alpha, n) =  
    """
    alpha = sqrt(2)
    beta = 1 / (1 - 1/alpha)
    n = float(str_n)
    m = floor(n * alpha)
    assert beattySum(alpha, m) + beattySum(beta, m) == m*(m+1)/2
    return ((m*(m+1)) / 2) - beattySum(beta, m)
    
    

# print solution('77') == 4208

# print solution('5') == 19

for i in range(1, int(pow(2,12))):
    j = str(i)
    assert solution(j) == tester(j), i
    # solution(j)
    print i

# print solution(str((10**100)+1))
