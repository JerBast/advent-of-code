from aocd import get_data


data = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
data = get_data(year=2023, day=22)
data = data.split('\n')

# Create bricks
bricks = []
for idx, row in enumerate(data):
    p1, p2 = row.split('~')
    p1 = list(map(int, p1.split(',')))
    p2 = list(map(int, p2.split(',')))

    bricks.append((idx, p1, p2))


def inefficient(bricks):
    # New bricks to be returned
    new_bricks = []

    # Keep track of visited points
    visited = set()

    # Sort bricks based on lowest y-index
    bricks.sort(key=lambda e: e[1][2])

    # Simulate process of falling
    for brick in bricks:
        idx, p1, p2 = brick
        x1, y1, z1 = p1
        x2, y2, z2 = p2

        if x1 != x2:
            # Lower height as far as possible, while ensuring no clash on the x-axis
            while z1 > 1 and all((x, y1, z1 - 1) not in visited for x in range(x1, x2 + 1)):
                z1, z2 = z1 - 1, z2 - 1
            
            # Store points
            for x in range(x1, x2 + 1):
                visited.add((x, y1, z1))
        elif y1 != y2:
            # Lower height as far as possible, while ensuring no clash on the y-axis
            while z1 > 1 and all((x1, y, z1 - 1) not in visited for y in range(y1, y2 + 1)):
                z1, z2 = z1 - 1, z2 - 1
            
            # Store points
            for y in range(y1, y2 + 1):
                visited.add((x1, y, z1))
        else:
            # Lower height as far as possible
            while z1 > 1 and (x1, y1, z1 - 1) not in visited:
                z1, z2 = z1 - 1, z2 - 1
            
            # Store points
            for z in range(z1, z2 + 1):
                visited.add((x1, y1, z))
        
        # Keep track of new bricks
        new_bricks.append((idx, (x1, y1, z1), (x2, y2, z2)))
    
    # Return new bricks
    return new_bricks


# Simulate gravity
bricks = inefficient(bricks)

# Remove bricks (one at a time)
# Verify that result is as expected (if steady) or deviates
ans1 = 0
ans2 = 0
expected = bricks.copy()
expected_set = set(expected)
for brick in bricks:
    # Remove brick from expectations
    expected.remove(brick)
    expected_set.remove(brick)

    difference = set(expected).difference(inefficient(expected))
    if len(difference) == 0:
        ans1 += 1
    else:
        ans2 += len(difference)
    
    # Reset state by adding brick
    expected.append(brick)
    expected_set.add(brick)

# Part 1 & 2
print(ans1)
print(ans2)
