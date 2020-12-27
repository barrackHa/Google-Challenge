def to2(n):
    lst = []
    for i in range(1,(n+(n%2))/2):
        #print(i)
        lst.append((n-i,i))
    return lst



def sol(n):
    a = [0 for i in range(n+1)]
    a[3] = 1
    for i in range(4,n+1):
        #print i, ' ', ((i/2)*2)-2
        if i%2 == 1:
            a[i] = a[i-2] + 1
        else:
            a[i] = a[i-1]   
    return a[n]

def ans(n):
    t = [[0 for _ in range(n+2)] for _ in range(n+2)]
    s = '{},{}'
    tmp = cases(1,n,t,s) - 1
    #for l in reversed(range(len(t))):
    # for l in t:
    #     print l
    return tmp

def cases(h,l,t,s):
    # print(s.format(h,l))
    s = ' '+s
    if t[h][l] != 0:
        return t[h][l]
    if l == 0:
        return 1
    if l<h:
        return 0
    t[h][l] = cases(h+1,l-h,t,s) + cases(h+1,l,t,s)
    # for j in reversed(range(len(t))):
    #     print(t(j))
    # input('\nh = {}, l = {} \n'.format(h,l))

    return t[h][l]

def calc(i,j,mem):
    if mem[i][j] != 0: return mem[i][j]
    #if j == 0: return 1
    if i == 0: return 1
    #if j < i: return 0
    if j >  i: return 0
    #mem[i][j] = calc(i+1,j-i,mem) + calc(i+1,j,mem)
    mem[i][j] = calc(i,j+i,mem) + calc(i-1,j+1,mem)
    return mem[i][j]

def calc2(h,l,mem,s):
    #print(s.format(h,l))
    s = ' '+s
    if mem[h][l] != 0: return mem[h][l]
    if l == 0: return 1
    if l<h: return 0
    mem[h][l] = calc2(h+1,l-h,mem,s) + calc2(h+1,l,mem,s)
    return mem[h][l]

def solution(n):
    mem = [[0 for _ in range(n+2)] for _ in range(n+2)]
    s = '{},{}'
    #tmp = calc(1,n,mem) - 1
    tmp = calc2(1,n,mem,s) -1
    # for l in mem:
    #     print l
    return tmp

def tmp(n):
    mem = [[0 for _ in range(n+2)] for _ in range(n+2)]
    for i in range(n+2):
        for j in range(n+2):
            mem[i][j] = 1 if j>=i  else 0
            #mem[i][j] = (i,j)
    for l in mem:
        print l

i = 200
#tmp(i)
print solution(i)
print ans(i)
# for i in range(3,201):  
#     if  ans(i) != solution(i):
#         print i
#         break
    # sol(i)

# 6 - (3,2,1)
# 7 - (4,2,1)
# 8 - (5,2,1), (4,3,1) 
# 9 - (6,2,1), (5,3,1), (4,3,2)
# 10 - (7,2,1), (6,3,1), (5,3,2), (5,4,1)
# 11 - (8,2,1), (7,3,1), (6,3,2), (6,4,1), (5,4,2) 
# 12 - (9,2,1), (8,3,1), (7,3,2), (7,4,1), (6,4,2), (6,5,1), (5,4,3)
# 13 - (10,2,1), (9,3,1), (8,3,2), (8,4,1), (7,5,1), (7,4,2), (6,5,2), (6,4,3)
# 14 - (11,2,1), (10,3,1), (9,4,1), (9,3,2), (8,5,1), (8,4,2), (7,6,1), (7,5,2), (7,4,3), (6,5,3) 