from decimal import Decimal, localcontext
from math import sqrt, floor

MAGNITUDE = 100
with localcontext() as ctx:
    ctx.prec = MAGNITUDE + 1
    sqrt2 = Decimal(2).sqrt()
    n1 = Decimal(1)
    a = int(str(sqrt2 - n1)[2:])

def solution(str_n):
    n = int(str_n)
    m = (a * n) // 10 ** MAGNITUDE #floor 
    tot = 0

    if n == 0:
        return tot
    else:
        tot = (n * m) + \
            ((n * (n + 1)) / 2) - \
            ((m * (m + 1)) / 2) -\
            int(solution(m))
        return str(tot)

def tester(str_n):
    sqrt2 = sqrt(2)
    n = float(str_n)
    tot, i = 0, 1
    while i <= n:
        tot += float(floor((i)*sqrt2))
        i += 1
    return str(tot)[:-2]


# print solution('5')
# print solution('77') == '4208'
# print solution('5') == '19'

fails = 0
for i in range(int(pow(2,0)), int(pow(2,11))):
    j = str(i)
    s, t = solution(j), tester(j)
    try:
        assert solution(j) == tester(j) , i
    except Exception as e:
        print int(s) - int(t)
        fails += 1
        break
print fails
