def caseCounter(i,j,mem):
    if mem[i][j] != 0: return mem[i][j]
    if j == 0: return 1
    if j<i: return 0
    mem[i][j] = \
        caseCounter(i+1,j-i,mem) \
        + caseCounter(i+1,j,mem)
    return mem[i][j]

def solution(n):
    mem = [[0 for _ in range(n+2)] for _ in range(n+2)]
    return caseCounter(1,n,mem) - 1
