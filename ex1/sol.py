#! python2
from math import sqrt

primesLst = [2,3]
primesStr = '23'
	
def isPrime(n):
	for q in range(2,int(sqrt(n))+1):
		if n%q == 0:
			return False
	return True	

def getNextPrime():
	global primesLst
	thisP = primesLst[-1]
	nextP = thisP + 2
	while not isPrime(nextP):
		nextP += 2
	return nextP

def genPrimesStr(i):
	global primesStr
	global primesLst
	while len(primesStr) < i+5:
		print("looping...")
		p = getNextPrime()
		primesLst.append(p)
		primesStr = primesStr + str(p)
	return primesStr


def solution(i):
	primes = genPrimesStr(i)
	return primes[i:i+5]

#print solution(10000)
#print "#"*40
#print solution(77)
#print solution(0)
print solution(1)
print solution(2)
print solution(3)
print solution(4)
print solution(5)
print solution(6)
#print primesStr