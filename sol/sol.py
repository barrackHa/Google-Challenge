#! python2
from math import sqrt
	
def isPrime(n):
	for q in range(2,int(sqrt(n))+1):
		if n%q == 0:
			return False
	return True	

def genPrimesLst(n):
    lst = []
    for i in range(2,20232):
	print "check ", i
	if isPrime(i):
	    lst.append(i)
    return lst


def solution(i):
	print("invoke genPrimesLst")
	primes = genPrimesLst(i+5+1)
	print "="*10, "  DONE  ", "="*10
	print primes[-1]
	print "len = ", len(primes)

solution(4)
