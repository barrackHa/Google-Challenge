def factorial(n):
    m = 1
    for i in range(1,n+1):
        m *= i
    return m

def nChoosK(n,k):
    return (factorial(n))/(factorial(n-k)*factorial(k))

def numOfOptions(n,k):
    return nChoosK(n-1,k)

print numOfOptions(4,2)

"""
#3 - len is 1
#4 - len is 1
#5 - len is 2
#6 - len is 3
#7 - len is 5
#8 - len is 7
#9 - len is 9
#10 - len is 12
#11 - len is 15
#12 - len is 20
#13 - len is 24
#14 - len is 30
#15 - len is 36
#16 - len is 45
#17 - len is 53
#18 - len is 65
#19 - len is 77
#20 - len is 91
#21 - len is 108
#22 - len is 128
#23 - len is 150
#24 - len is 176
#25 - len is 206
#26 - len is 239
#27 - len is 279
#28 - len is 322
#29 - len is 373
#30 - len is 431
#31 - len is 497
#32 - len is 569
#33 - len is 655
#34 - len is 749
#35 - len is 856
#36 - len is 977
#37 - len is 1114
#38 - len is 1266
#39 - len is 1440
#40 - len is 1633
#41 - len is 1849
#42 - len is 2093
#43 - len is 2365
#44 - len is 2667
#45 - len is 3008
#46 - len is 3387
#47 - len is 3807
#48 - len is 4279
#49 - len is 4801
#50 - len is 5381
#51 - len is 6028
#52 - len is 6744
#53 - len is 7536
#54 - len is 8418
#55 - len is 9391
#56 - len is 10468
#57 - len is 11661
#58 - len is 12977
#59 - len is 14427
#60 - len is 16033
#61 - len is 17799
#62 - len is 19743
#63 - len is 21889
#64 - len is 24247
#65 - len is 26837
#66 - len is 29690
#67 - len is 32819
#68 - len is 36253
#69 - len is 40025
#70 - len is 44158
#71 - len is 48684
#72 - len is 53648
#73 - len is 59078
#74 - len is 65016
#75 - len is 71518
#76 - len is 78620
#77 - len is 86375
#78 - len is 94852
#79 - len is 104099
#80 - len is 114185
#81 - len is 125191
#82 - len is 137181
#83 - len is 150241
#84 - len is 164473
#85 - len is 179959
#86 - len is 196805
#87 - len is 215137
#88 - len is 235061
"""