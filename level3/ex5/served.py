def longer(lst):
    cases = []
    for c in lst:
        if 1 < c[-1]:
            new = c[:]
            new.append(1)
            cases.append(new)
    return cases

def higher(lst):
    cases = []
    for c in lst:
        if len(c) < 2:
            continue
        for i in range(len(c)):
            if i == 0:
                new = c[:]
                new[0] += 1
                if new not in cases:
                    cases.append(new)
            if c[i]+1 < c[i-1]: 
                new = c[:]
                new[i] += 1
                if new not in cases:
                    cases.append(new)
    return cases

def sol(n):
    if n in [1,2]:
        return[[n]]
    less = sol(n-1)
    cases = []
    cases += longer(less)
    cases += higher(less)
    return cases

def solution(n):
    return len(sol(n))

print solution(3)