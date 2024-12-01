import re

from aocd import get_data


def count_possibilities(s: str, pattern: list[int]):
    if '?' in s:
        return count_possibilities(s.replace('?', '.', 1), pattern) + count_possibilities(s.replace('?', '#', 1), pattern)
    
    return int(list(map(len, re.findall('#+', s))) == pattern)


def count_all(s: str, defect: list[int], visited: dict[str, int] = {}):
    # Normalize input string
    s = '.'.join(re.split('\.+', s.strip('.')))

    # Check if we have a memorized result
    s_id = s + str(defect)
    if s_id in visited:
        return visited[s_id]
    
    # Check if the string matches the pattern leading to a valid result
    # If not, return faulty occurrence
    if not re.match('[\.\?#]*' + '[\.\?]+'.join(f'[#\?]{{{d}}}' for d in defect), s):
        visited[s] = 0
        return 0

    # Matches and no unknowns left, this is a keeper
    if '?' not in s:
        visited[s_id] = 1
        return 1
    
    # Accumulate result of paths while eliminating targets
    target = '#' * defect[0]
    res = 0

    # Branch with '?' replaced by '.'
    s1 = s.replace('?', '.', 1).strip('.')
    s1_vals = s.split('.')
    if s1_vals[0].startswith(target):
        # TODO: partial match handling
        res += count_all('.'.join(s1_vals[:]), defect, visited)
    else:
        # No match after replacement, continue
        res += count_all(s1, defect, visited)

    # Branch with '?' replaced by '#'
    s2 = s.replace('?', '#', 1)
    s2_vals = s.split('.')
    if s2_vals[0].startswith(target):
        # TODO: partial match handling
        pass
    else:
        # No match after replacement, continue
        res += count_all(s2, defect, visited)
    
    # Return the result
    return res

    # Accumulate result of paths
    # res = count_all(s.replace('?', '.', 1), defect, visited) + count_all(s.replace('?', '#', 1), defect, visited)
    # visited[s] = res
    # return res




def count_pos(free: list[str], remaining: list[int]):
    if sum(map(len, free)) < sum(remaining):
        # Terminate if there is no chance at winning the game
        return 0

    print(free, remaining)
    if len(remaining) == 0:
        # Nothing is remaining, valid fit
        print(1)
        return 1
    if len(free) == 0:
        # No space, but something remaining, invalid fit
        return 0

    space = free[0]
    required = remaining[0]
    space_len = len(space)
    
    if space_len < required:
        # Does not fit, skip to next
        return count_pos(free[1:], remaining)
    elif space_len == required:
        # Space fits perfectly, try next one (including future placing)
        return count_pos(free[1:], remaining) + count_pos(free[1:], remaining[1:])
    
    # Lots of space remaining, try all
    res = 0
    res += count_pos(free[1:], remaining[1:])                              # We accept for this position
    res += count_pos([space[1:]] + free[1:], remaining)                    # We continue, do not take position

    if space[required] == '?' and len(space) > required + 1:               # Only if no clash is caused, and space available
        res += count_pos([space[required + 1:]] + free[1:], remaining[1:]) # We accept and attempt to fit in remaining space
    return res


data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
# data = """#.#.### 1,1,3
# .#...#....###. 1,1,3
# .#.###.#.###### 1,3,1,6
# ####.#...#... 4,1,1
# #....######..#####. 1,6,5
# .###.##....# 3,2,1"""
# data = get_data(year=2023, day=12)

# tot = 0
# ans = 0
# for row in data.split('\n')[1:]:
#     springs, damaged = row.split()
#     damaged = list(map(int, damaged.split(',')))

#     tot += count_possibilities(springs, damaged)

#     ans += count_all(springs, damaged)
#     print(tot, ans)
#     exit()

# print(tot)
# print(ans)
# 6871

D = get_data(year=2023, day=12)
L = D.split('\n')
G = [[c for c in row] for row in L]

# i == current position within dots
# bi == current position within blocks
# current == length of current block of '#'
# state space is len(dots) * len(blocks) * len(dots)
DP = {}
def f(dots, blocks, i, bi, current):
  key = (i, bi, current)
  if key in DP:
    return DP[key]
  if i==len(dots):
    if bi==len(blocks) and current==0:
      return 1
    elif bi==len(blocks)-1 and blocks[bi]==current:
      return 1
    else:
      return 0
  ans = 0
  for c in ['.', '#']:
    if dots[i]==c or dots[i]=='?':
      if c=='.' and current==0:
        ans += f(dots, blocks, i+1, bi, 0)
      elif c=='.' and current>0 and bi<len(blocks) and blocks[bi]==current:
        ans += f(dots, blocks, i+1, bi+1, 0)
      elif c=='#':
        ans += f(dots, blocks, i+1, bi, current+1)
  DP[key] = ans
  return ans

for part2 in [False,True]:
  ans = 0
  for line in L:
    dots,blocks = line.split()
    if part2:
      dots = '?'.join([dots, dots, dots, dots, dots])
      blocks = ','.join([blocks, blocks, blocks, blocks, blocks])
    blocks = [int(x) for x in blocks.split(',')]
    DP.clear()
    score = f(dots, blocks, 0, 0, 0)
    #print(dots, blocks, score, len(DP))
    ans += score
  print(ans)
