from colorama import Fore, Style
from collections import deque
import mmap
from typing import Deque


def search(file_map, pattern, history=1):
  line_queue = deque(maxlen=history+1)
  found = False
  count_down = history

  for line in iter(file_map.readline, b''):
    word_in_line = line.find(str.encode(pattern))
    if word_in_line != -1:
      coloured = f'{Fore.GREEN}{pattern}{Style.RESET_ALL}'
      found = True
      count_down = history
      line_queue.append(line.strip(b'\n').decode().replace(pattern, coloured))
      if len(line_queue) == history+1:
        yield line_queue
        line_queue.clear()
    elif found:
      line_queue.append(line.strip(b'\n').decode())
      count_down -= 1
      # if queue is full
      if len(line_queue) == history+1:
        yield line_queue
        line_queue.clear()
      # if count down is at 0 
      if not count_down:
        yield line_queue
        line_queue.clear()
        found = False
    else:
      line_queue.append(line.strip(b'\n').decode())
  if found:
    yield line_queue


if __name__ == '__main__':
  with open('test.txt', mode='r', encoding='utf8') as file_obj:
    with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
      for lines in search(mmap_obj, pattern='Hello', history=4):
        for pline in lines:
          print(pline)