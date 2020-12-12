
def addOne(n):
    if len(n) == 0:
        return '1'
    else:
        lastDig = int(n[-1])
    lastDig += 1
    if lastDig < 10:
        return n[:-1] + str(lastDig)
    else:
        return addOne(n[:-1]) + '0'

def subtactOne(n):
    lastDig = int(n[-1])
    if lastDig == 0:
        tmp = subtactOne(n[:-1]) + '9'
        return tmp.lstrip('0')
    else:
        lastDig -= 1
        return n[:-1] + str(lastDig)
    
def divisionRecursion(n):
    if len(n) == 1:
        return str(int(n)/2)
    firstDig = int(n[0])
    if firstDig%2 == 0:
        firstDig /= 2
        return str(firstDig) + divisionRecursion(n[1:])
    else:
        firstDig /= 2
        rest = divisionRecursion(n[1:])
        secDig = str(int(rest[0])+5)
        tmp = str(firstDig) + secDig + rest[1:]
        return tmp

def divideByTwo(n):
    return divisionRecursion(n).lstrip('0')

def sol(n):
    if n == '1':
        return 0
    elif int(n[-1])%2 == 0:
        return sol(divideByTwo(n)) + 1
    else:
        return min(\
            sol(addOne(n)),\
            sol(subtactOne(n))\
        )+1


def toBinary(n):
    """
        Takes a string n representing a number >= 0 in base 10.
        Returns a string of n's binary representation.
    """
    if n in ['0','1']:
        return n
    dig = '0' if int(n[-1])%2 == 0 else '1'
    tmp = n if dig == '0' else subtactOne(n)
    return toBinary(divideByTwo(tmp)) + dig 

def binaryAddOne(n):
    if len(n) == 0:
        return '1'
    lastDig = int(n[-1])
    if lastDig == 0:
        return n[:-1] + '1'
    else:
        return binaryAddOne(n[:-1]) + '0'

def binaryHelper(b):
    if b == '1': 
        return 0
    elif b.endswith('0'):
        return binaryHelper(b[:-1]) + 1
    elif b.endswith('111'):
        return binaryHelper(binaryAddOne(b)) + 1
    else:
        # print(b)
        return binaryHelper(b[:-1]+'0') + 1

def solution(n):
    return 0 if n == '1' else binaryHelper(toBinary(n))

print toBinary('59')
print sol('59')
print solution('59')
# print sol(str(2))
# print sol(str(3))
# print sol(str(4))
# print sol(str(15))

# print toBinary('0')
# print toBinary('1')
# print toBinary('2')

# print binaryAddOne('0')
# print binaryAddOne('1')
# print binaryAddOne(toBinary('11'))

# for i in range(1,49999):
#     s = binaryAddOne(toBinary(str(i)))
#     if bin(i+1)[2:] != s:
#         print i
#         break
# biggest = '9' * 309
# print '#'*30
# print solution(str(1))
# print solution(str(2))
# print solution(str(3))
# print solution(str(4))
# print solution(str(15))

# for i in range(1,499):
#     n = str(i)
#     s1 = sol(n)
#     s2 = solution(n)
#     if s1 != s2:
#         print n
#         #break

print sol('9'*100)
        
