import math
import re
s = '5.02x^2 + 2x + 10 + 5.02x^2'
print(re.sub(r'([a-zA-Z])\^(\d+)', r'Math.pow(\1,\2)', re.sub(r'(\d)([a-zA-Z])', r'\1*\2', s)))
