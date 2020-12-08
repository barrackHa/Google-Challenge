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
    leftWalkers = salutes = 0
    for c in s:
        if c == '>':
            leftWalkers += 1
        elif c == '-':
            continue
        else:
            salutes += 2 * leftWalkers
    return salutes

#exampleFileBuilder(1000000,newFile=False)
#print(sol('>----<'))
#print(sol("<<>><"))
#print(sol("--->-><-><-->-"))
#print(sol3('>----<'))
#print(sol3("<<>><"))
#print(sol3("--->-><-><-->-"))

with open('./ex3/examples.txt','r') as f:
    print('starting tests...')
    tot_diffs = tot_lines = 0
    for l in f:
        l = l.strip('\n')
        tot_lines += 1
        if not (sol(l) == sol3(l)):
            print(l)
            tot_diffs += 1
        if tot_lines % 100000 == 0:
            print('Checked {} lines, so far {} diffs'.format(tot_lines, tot_diffs))
    print(tot_diffs, ' diffs found between sol and sol3')



