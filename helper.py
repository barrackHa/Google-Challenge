import urllib.request
import json

url = 'http://sethriedel.com/primes/api/primes.php?limit='
limit = 20210

def responseJSON(url):
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode('utf-8'))

primesStr = ''
primesLst = []

while (len(primesStr) < 10007):
    limit += 2
    res = responseJSON(url + str(limit))
    primesLst = [str(p) for p in res['primes']]
    primesStr = ''.join(primesLst)
    print('limit = ', limit, ' len = ', len(primesStr), ' last p = ', primesLst[-1])

print(primesLst[-10:])
print('limit = ', limit, ' s_len = ', len(primesStr), ' lst_len = ', len(primesLst))
#print(str(res['primes']))
#print(json.dumps(res['primes'], indent=4, sort_keys=True))

"""
Results:
limit =  20212  len =  9999  last p =  20201
limit =  20214  len =  9999  last p =  20201
limit =  20216  len =  9999  last p =  20201
limit =  20218  len =  9999  last p =  20201
limit =  20220  len =  10004  last p =  20219
limit =  20222  len =  10004  last p =  20219
limit =  20224  len =  10004  last p =  20219
limit =  20226  len =  10004  last p =  20219
limit =  20228  len =  10004  last p =  20219
limit =  20230  len =  10004  last p =  20219
limit =  20232  len =  10009  last p =  20231
['20143', '20147', '20149', '20161', '20173', '20177', '20183', '20201', '20219', '20231']
limit =  20232  s_len =  10009  lst_len =  2287
"""


