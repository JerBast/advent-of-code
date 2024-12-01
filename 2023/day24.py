from aocd import get_data


def part1(p1, d1, p2, d2):
    dp = [p1[i] - p2[i] for i in range(3)]
    dd = [d1[i] - d2[i] for i in range(3)]
    if all(e == 0 for e in dp):
        return 200000000000000 <= p1[0] <= 400000000000000 and 200000000000000 <= p1[1] <= 400000000000000

    a = dp[0] / dd[0]
    b = dp[1] / dd[1]
    c = dp[2] / dd[2]
    if a == b and b == c:
        x = p1[0] + a * d1[0]
        y = p1[1] + a * d1[1]
        # z = p1[2] + a * d1[2]
        return 200000000000000 <= x <= 400000000000000 and 200000000000000 <= y <= 400000000000000
    return False


data = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
# data = get_data(year=2023, day=24)
data = data.split('\n')

hail = []
for row in data:
    origin, direction = row.split(' @ ')
    origin = tuple(map(int, origin.split(', ')))
    direction = list(map(int, direction.split(', ')))
    hail.append((origin, direction))

c = 0
for i in range(len(hail)):
    p1, d1 = hail[i]
    for j in range(i + 1, len(hail)):
        p2, d2 = hail[j]
        c += part1(p1, d1, p2, d2)
print(c)
