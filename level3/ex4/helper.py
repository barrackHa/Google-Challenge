def test(n):
    n = long(n)
    steps = 0
    while n != 1:
        if n%2 == 0:
            n /= 2
        elif n == 3 or n%4 ==1:
            n -= 1
        else:
            n += 1
        steps += 1
    return steps

#for i in range(2,21):
#    print '{} -> {}, sol =  {}'.format(i, bin(i)[2:],test(i))

# for i in range(1,100):
#     if i%4 == 3:
#         print '{} -> {}'.format(i, bin(i)[2:])

print test('9'*309)