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
    transOps = 0 
    while b != '1':
        if b[-1] == '0':
            b = b[:-1] #division of an even binary
        elif b[-3:] == '111' or b[-3:] == '011':
            #Counting the num of ops needed to deal with
            #'111' or '011' shows 
            #adding 1 gives at least the same if not
            #better num results.
            b = binaryAddOne(b)
        else:
            b = b[:-1]+'0' #subtract 1 from odd binary 
        transOps += 1
    return transOps
