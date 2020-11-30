#! python
from math import sqrt
	
def isPrime(n):
	for q in range(2,int(sqrt(n))+1):
		if n%q == 0:
			return False
	return True	

def genPrimesStr(n):
    lst = ''
	#while (len(lst)<n):
    	#getNextPrime()
    
	#return 


def solution(i):
	primes = genPrimesStr(i+5+1)
	print isPrime(7)

solution(4)
