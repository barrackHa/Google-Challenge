from random import randint

def sol(s):
    counter = 0
    for i in range(len(s)): 
        if s[i] == '>':
            for d in s[i:]:
                counter = counter+1 if d=='<' else counter
    return 2*counter

def exampleFileBuilder(numOfExamplesToGen, newFile=False):
    fileUsage = 'w' if newFile else 'a'
    f = open('./ex3/examples.txt', fileUsage)
    while(numOfExamplesToGen > 0):
        strLen = randint(1,100)
        tmpS = ''
        for i in range(strLen):
            tmpS += ['-','<','>'][randint(0,2)]
        f.write(tmpS+'\n')
        numOfExamplesToGen -= 1
    f.close()
    return

def sol3(s):
    leftWalkers = 0
    salutes = 0
    for c in s:
        if c == '>':
            leftWalkers += 1
        elif c == '-':
            continue
        else:
            salutes += 2 * leftWalkers
    return salutes

#exampleFileBuilder(100000,newFile=True)
#print(sol('>----<'))
#print(sol("<<>><"))
#print(sol("--->-><-><-->-"))
#print(sol3('>----<'))
#print(sol3("<<>><"))
#print(sol3("--->-><-><-->-"))

with open('./ex3/examples.txt','r') as f:
    tot = 0
    for l in f:
        l = l.strip('\n')
        if not (sol(l) == sol3(l)):
            print(l)
            tot += 1
    print(tot, ' diffs found between sol and sol3')



