import numpy as np

from aocd import get_data

data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
data = get_data(year=2023, day=9)

# Part 1
ans = 0
for history in data.split('\n'):
    readings = list(map(int, history.split()))
    next_val = 0
    
    while np.any(readings):
        next_val += readings[-1]
        readings = np.diff(readings)
    
    ans += next_val
print(ans)

# Part 2
ans = 0
for history in data.split('\n'):
    readings = list(map(int, history.split()))
    next_vals = []
    
    while np.any(readings):
        next_vals.append(readings[0])
        readings = np.diff(readings)
    
    next_val = 0
    for val in next_vals[::-1]:
        next_val = val - next_val
    ans += next_val
print(ans)
