# def sol(n):
#     #b = bin(int(n))
#     a_byte_array = bytearray(n, "utf8")
#     byte_list = []
#     print a_byte_array
#     for byte in a_byte_array:
#         binary_representation = bin(byte)
#         byte_list.append(binary_representation)
#     return byte_list



# 
def sol(n):
    b = long(n)
    s = 0
    if b == 1:
        return 0
    elif b%2 == 0:
        return sol(str(b/2))+1
    else:
        return min(sol(str(b+1)), sol(str(b-1)))+1

print sol(str(4))
#print sol(str(15))
print sol(str(2**1026+2**1024+2**1023+2**1020))


#for i in range(2,200):
    #s1 = sol(str(i))
    #print '{} -> {}'.format(i,sol(str(i)))
    #s2 = sol(str(i+1))+1
    #if s2 < s1:
    #    print i, ' -> {} -> s1 = {}, s2 = {}'.format(bin(i),s1,s2)  