import numpy as np

a = [
  [0,1/2,0,0,0,1/2],  
  [4/9,0,0,3/9,2/9,0],  
  [0,0,1,0,0,0],  
  [0,0,0,1,0,0],  
  [0,0,0,0,1,0],  
  [0,0,0,0,0,1],  
]

b = np.array(a)
f = lambda x: x.dot(x)

for i in range(1000):
    b = f(b)
    #print(b,'\n\n')

from fractions import Fraction
# for r in list(b):
#     for e in list(r):
#         print(str(Fraction(r)), end=' ')
#         #print(r, end='\n')
#     print()
print(b)
l = [\
    0.21428571, 0.14285714, 0.64285714,\
    0.42857143, 0.28571429, 0.28571429\
]
for n in l:
    print(str(Fraction(n)), end='\n')
print(3/14, 9/14)