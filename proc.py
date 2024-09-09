import sys
import time

import tqdm

print("hello world")

for i in tqdm.trange(50, file=sys.stdout):
    time.sleep(0.1)
    print("我是傻逼")

print("bye world")
