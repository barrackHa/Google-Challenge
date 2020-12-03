def sol(s):
    counter = 0
    for i in range(len(s)): 
        if s[i] == '>':
            for d in s[i:]:
                counter = counter+1 if d=='<' else counter
    return 2*counter


print(sol('>----<'))
print(sol("<<>><"))
print(sol("--->-><-><-->-"))
