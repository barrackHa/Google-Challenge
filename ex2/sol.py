
def sol(x,y):
    diagNum = x+y-1 
    diagStartsWith = ((diagNum * (diagNum - 1)) / 2) + 1
    stepsOnDiag = x - 1
    return str(diagStartsWith + stepsOnDiag)


print(sol(1,1), sol(1,2), sol(1,3), sol(1,4))  
print(sol(2,1), sol(2,2), sol(2,3)) 
print(sol(3,1), sol(3,2), sol(3,3))
print(sol(4,1), sol(4,2)) 
print(sol(5,1), sol(5,2)) 
print(sol(5+1,1)) 
