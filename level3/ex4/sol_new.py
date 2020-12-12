def subtractOne(n):
    lastDig = int(n[-1])
    if lastDig == 0:
        tmp = subtractOne(n[:-1]) + '9'
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

# def toBinary(n):
#     """
#         Takes a string n representing a number >= 0 in base 10.
#         Returns a string of n's binary representation.
#     """
#     if n in ['0','1']:
#         return n
#     dig = '0' if int(n[-1])%2 == 0 else '1'
#     tmp = n if dig == '0' else subtractOne(n)
#     return toBinary(divideByTwo(tmp)) + dig 

def toBinary(n):
    """
        Takes a string n representing a number >= 0 in base 10.
        Returns a string of n's binary representation.
    """
    if n in ['0','1']:
        return n
    dig = '0' if int(n[-1])%2 == 0 else '1'
    #tmp = n if dig == '0' else subtractOne(n)
    return toBinary(n[:-1]) + dig

def binaryAddOne(n):
    if len(n) == 0:
        return '1'
    lastDig = int(n[-1])
    if lastDig == 0:
        return n[:-1] + '1'
    else:
        return binaryAddOne(n[:-1]) + '0'

def solution(n): 
    b = bin(long(n))[2:]
    steps = 0 
    while b != '1':
        if b[-1] == '0':
            b = b[:-1] #division of an even binary
        elif b[-3:] == '111' or b[-3:] == '011':
            b = binaryAddOne(b)
        else:
            b = b[:-1]+'0' #subtract 1 from odd binary 
        steps += 1
    return steps


# print solution('1')        
# print solution('2')
# print solution('3')
# print solution('4')
# print solution('15')

print toBinary('3')
for i in range(1,11):
    print toBinary(str(i))