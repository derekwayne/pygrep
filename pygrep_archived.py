def colour_word(word: str, sw_pos: int, line: str) -> str:
  head, tail = line[:sw_pos], line[sw_pos+len(word):]
  return f'{head}{Fore.GREEN}{word}{Style.RESET_ALL}{tail}'


def print_out_queue(q: Deque[str]) -> None:
  """Send contents of queue to standard output"""
  while q:
    print(q.popleft())



def mmap_io(filename: str, word: str, N: int) -> None:
  with open(filename, mode='r', encoding='utf8') as file_obj:
    with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
      
      line_queue = deque([], maxlen=N)
      word_matched = False  # bool to track if we need to print N lines after match
      n_lines_seen_after = 0

      for line in iter(mmap_obj.readline, b''):

        sw_pos = line.find(str.encode(word))

        # IF WORD IN LINE
        # TODO: highlight all word matches not just first
        if sw_pos != -1:

          coloured = colour_word(word=word, sw_pos=sw_pos, line=line.strip(b'\n').decode())
          # empty the queue by printing the lines before target line
          print_out_queue(line_queue)
          # print line with match
          print(coloured)

          word_matched = True
          n_lines_seen_after = 0

        
        # IF WORD IS NOT IN THE LINE
        else:
          # check if we need to print N lines after a previous match
          if word_matched:
            line_queue.append(line.strip(b'\n').decode())
            n_lines_seen_after += 1  # update # lines seen after a match

            if n_lines_seen_after == N:
              print_out_queue(line_queue)
              word_matched = False

          else:
            line_queue.append(line.strip(b'\n').decode())
      
      # If there are lines that still need to be printed at the end
      if word_matched:
        print_out_queue(line_queue)