import sys

sys.setrecursionlimit(3000)
# def sol(n):
#     #b = bin(int(n))
#     a_byte_array = bytearray(n, "utf8")
#     byte_list = []
#     print a_byte_array
#     for byte in a_byte_array:
#         binary_representation = bin(byte)
#         byte_list.append(binary_representation)
#     return byte_list


def sol1(n):
    b = long(n)
    if b == 1:
        return 0
    elif b%2 == 0:
        return sol(str(b/2))+1
    else:
        return min(sol(str(b+1)), sol(str(b-1)))+1

def sol2(n):
    b = long(n)
    if b == 1:
        return 0
    elif b%2 == 0:
        return min(sol(str(b/2)), sol(str(b+1)), sol(str(b-1)))+1
    else:
        return min(sol(str(b+1)), sol(str(b-1)))+1


def binaryHelper(b):
    if b == bin(1):
        return 0
    elif b[-1] == '0':
        return binaryHelper(b[:-1])+1
    elif b[-2:] == '11' and len(b[:-2])>2:
        return binaryHelper(bin(long(b,2)+1)) + 1
    else:
        return binaryHelper(bin(long(b,2)-1)) + 1


def sol(n):
    b = bin(long(n))
    return binaryHelper(b)


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

def subtrectOne(n):
    lastDig = int(n[-1])
    if lastDig == 0:
        tmp = subtrectOne(n[:-1]) + '9'
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
        #print '--- ', firstDig, ' | ', n[1:]
        return str(firstDig) + divisionRecursion(n[1:])
    else:
        firstDig /= 2
        rest = divisionRecursion(n[1:])
        secDig = str(int(rest[0])+5)
        tmp = str(firstDig) + secDig + rest[1:]
        return tmp

def divideByTwo(n):
    return divisionRecursion(n).lstrip('0')

def solution(n):
    if n == '1':
        return 0
    elif int(n[-1])%2 == 0:
        return solution(divideByTwo(n)) + 1
    else:
        return min(\
            solution(addOne(n)),\
            solution(subtrectOne(n))\
        )+1

print solution(str(1))
print solution(str(2))
print solution(str(3))
print solution(str(4))
print solution(str(15))

#print divideByTwo(str(2))

# for i in range(1,39121):
#     n = 2*i
#     if str(n/2) != divideByTwo(str(n)):
#         print n, " -> ", divideByTwo(str(n))
        
        

biggest = '9' * 309
print solution(biggest)
#print len(divideByTwo(addOne(biggest)))
#print addOne(biggest)
# print sol(biggest)
# print sol1(biggest)
# print sol2(biggest)
# print long(biggest)

# print sol2(str(1))
# print sol2(str(2))
# print sol2(str(3))
# print sol2(str(4))
# print sol2(str(15))
# print long('11111',2), sol2(long('11111',2))
# print sol2(32)
# print sol2(str(2**700+1))
# print sol2(str(2**1026+2**1024+2**1023+2**1020+3))


# for i in range(1,200):
#     s1 = sol1(str(i))
#     s2 = sol2(str(i))
#     if s2 != s1:
#         print i, ' -> {} -> s1 = {}, s2 = {}'.format(bin(i),s1,s2)  


