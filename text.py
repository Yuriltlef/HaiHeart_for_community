from HaiHeart_main.haibasetools import HaiLogs
import time
from HaiHeart_main.haibasetools import HaiVector
from random import random

g = HaiLogs()
for i in range(10000):
    
    time.sleep(0)
    g.log_out()

# h = []
# for i in range(1000):
#     h.append(HaiVector([random(), random(), random()]))

# for v in h:
#     print(v)

input()
