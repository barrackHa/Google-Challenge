"""
For an irrational real alpha > 0, the sequence
(alpha, n) = floor(alpha * n) is called the Beatty sequence.
Theorem (Beatty): let beta be an irrational real number such that if:
alpha^-1 + beta^-1 = 1 then {beatty(alpha, n) | n in {1,2,...}} and
{beatty(beta, n) | n in {1,2,...}} are a disjoint cover of all Natural numbers.
(more on the Beatty theorem - https://arxiv.org/pdf/1103.5198.pdf)
 
Denote S(alpha, n) = sum(beatty(alpha,1),....,beatty(alpha,n)), the sum
of first n elements of the beatty sequence.
 
Let a,b real numbers that satisfy the Beatty theorem conditions. 
Denote m := floor(a*n). Then - 
S(a,n) + S(b, floor(m/b)) = (m*(m+1))/2 
as a corollary of the Beatty theorem. 

We choose to have a = sqrt(2) and b = 2 + sqrt(2) (satisfies the Beatty theorem conditions). 
Also, for every n, it holds that - floor(m/b) = floor((a - 1) * n). 
Denote n_ := floor((a - 1) * n).
Plug it into the expression in former paragraph and we get - 
S(a,n) = (n+n_)*(n+n_+1)/2 - S(b,n_)

observation: S(b,n_) = S(a,n_) + n_*(n_ + 1) for every naturel n.

And so - S(a,n) = (n+n_)*(n+n_+1)/2 - n_*(n_ + 1) - S(a,n_) 
Alternatively - S(a,n) = n*n_ + n*(n+1)/2 - n_*(n_+1)/2 - S(a,n_)

This is a recursion formula to compute the Beatty sums. 
 
As n_ diminishes by a-1 (~ 1/2) at each iteration, for n's of magnitude 10**100,
we expect a magnitude of log(base 2)(10*100) iterations to complete the calculation.
"""

from decimal import Decimal, localcontext
from math import sqrt, floor

MAGNITUDE = 100
# Get the first 100 digits of sqrt(2) - 1
with localcontext() as ctx:
    ctx.prec = MAGNITUDE + 1
    sqrt2 = Decimal(2).sqrt()
    one = Decimal(1)
    sqrt2MinusOne = int(str(sqrt2 - one)[2:]) 

def solution(str_n):
    """Return the sum of n first elements of the Beatty sequence gen by sqrt(s)"""
    n = int(str_n)
    # Integer division by google gives the floor value becuase the calc
    # is made on sqrt2MinusOne as a 100 digits long int. 
    n_ = (sqrt2MinusOne * n) // (10 ** MAGNITUDE) 
    tot = 0

    if n == 0:
        return tot
    else:
        tot = (n * n_) + \
            ((n * (n + 1)) / 2) - \
            ((n_ * (n_ + 1)) / 2) -\
            int(solution(n_))
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
for i in range(int(pow(2,0)), int(pow(2,12))):
    j = str(i)
    s, t = solution(j), tester(j)
    try:
        assert solution(j) == tester(j) , i
    except Exception as e:
        print e
        print int(s) - int(t)
        fails += 1
        break
print fails
