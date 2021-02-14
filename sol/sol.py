from math import sqrt, floor

sqrt2 = sqrt(2)
# print floor(sqrt2)
def solution(str_n):
    n = float(str_n)
    tot, i = 0, 1
    while i <= n:
        tot += float(floor((i)*sqrt2))
        # print '{0}) floor(({0})*sqrt2) == {1}'.format(i, floor((i)*sqrt2))
        print '{0}) {0}*sqrt2 == {1}'.format(i, (i)*sqrt2)
        assert floor((i)*sqrt2) == (i*sqrt2) - ((i*sqrt2)%1)
        i += 1
    print(tot, (n**2)/sqrt2)
    return tot

def tmp(n):
    i = 1
    while i <= n:
        print i*sqrt2 - floor(i*sqrt2)
        i+=1
    

# print solution('77') == 4208

tmp(10)
# print solution('5') == 19

# print solution(str((10**100)+1))
