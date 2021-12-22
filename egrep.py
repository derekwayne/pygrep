from collections import deque
from colorama import Fore, Style
import mmap

def flushQueue(queue):
    while len(queue) != 0:
        print(queue.popleft(), end="")


nlines = 1
match = "world"
colored = f'{Fore.GREEN}{match}{Style.RESET_ALL}'
queue = deque(maxlen=nlines)
counter = -1
with open('test.txt', mode='r', encoding='utf8') as tst:
    with mmap.mmap(tst.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
      for l in iter(mm.readline, b''):
        if counter == 0:
            flushQueue(queue)
        elif counter != -1:
            counter = counter - 1


        s = l.strip(b'\n').decode().replace(match, colored)
        if s != l:
            flushQueue(queue)
            print(s, end="\n")
            counter = nlines
        else:
            queue.append(l.strip(b'\n').decode())


if counter != -1:
    flushQueue(queue)