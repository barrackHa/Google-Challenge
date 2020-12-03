"""
1  2  4  7 11 16
3  5  8  12 17
6  9  13 18
10 14 19
15 20
21
"""

def sol(x,y):
    diagNum = x+y-1 
    diagStartsWith = int(((diagNum * (diagNum - 1)) / 2) + 1)
    stepsOnDiag = x - 1
    ans = str(diagStartsWith + stepsOnDiag)
    return ans if len(ans)>1 else '0'+ans 


for i in range(1,20):
    for j in range(1,20-i):
        #print((i,j), end=' ')      
        print(sol(i,j), end=' ')     
    print()  