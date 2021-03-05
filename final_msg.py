import base64
from itertools import cycle

msg = 'OUYBFAgKAAoxRlJbS04CCycABkZHSUIaLQ0eBAoOEBxlQUhBTAwWDScEHwQPTklZZQQUBwQbEQpl QUhBTAALGjAEFggJBQBebkFVAAgBDBw0BB8EBR1CWXhBVRQFBQoaKQQWRkdJQgsjAxAIHxpCWXhB VRIKDwBebkFVBwQGQll4QVUWAgdEXj8='

key = bytes('barakiey','utf8')
dmsg = bytes(a ^ b for a, b in zip(base64.b64decode(msg), cycle(key))) 
print(dmsg.decode("utf-8"))

