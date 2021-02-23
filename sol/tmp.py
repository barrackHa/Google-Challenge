from math import sqrt, floor

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
    alpha = sqrt(2)
    beta = 1 / (1 - 1/alpha)
    n = float(str_n)
    m = floor(n * alpha)
    return str(((m*(m+1)) / 2) - beattySum(beta, m))[:-2]

def tester(str_n):
    sqrt2 = sqrt(2)
    n = float(str_n)
    tot, i = 0, 1
    while i <= n:
        tot += float(floor((i)*sqrt2))
        i += 1
    return str(tot)[:-2]

for i in range(1, int(pow(2,12))):
    j = str(i)
    assert solution(j) == tester(j), i
    # solution(j)
    print i