def sol(s):
    rightWalkers = 0
    salutes = 0
    for c in s:
        if c == '>':
            rightWalkers += 1
        elif c == '-':
            continue
        else:
            salutes += 2 * rightWalkers
    return salutes


print(sol('>----<'))
print(sol("<<>><"))
print(sol("--->-><-><-->-"))
print(sol('<<<<<<>>>>>>'))
