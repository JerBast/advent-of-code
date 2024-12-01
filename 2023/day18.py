from shapely import Polygon
from aocd import get_data


data = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
data = get_data(year=2023, day=18)

point = (0, 0)
points = []
for row in data.split('\n'):
    d, s, c = row.split()
    s = int(s)

    if d == 'R':
        point = (point[0] + s, point[1])
    elif d == 'L':
        point = (point[0] - s, point[1])
    elif d == 'U':
        point = (point[0], point[1] + s)
    else:
        point = (point[0], point[1] - s)

    points.append(point)

pol = Polygon(points)
print(pol.length + pol.area - pol.length // 2 + 1)




point = (0, 0)
points = []
for row in data.split('\n'):
    d, s, c = row.split()
    d = int(c[-2])
    s = int(c[2:-2], 16)

    if d == 0:
        point = (point[0] + s, point[1])
    elif d == 2:
        point = (point[0] - s, point[1])
    elif d == 3:
        point = (point[0], point[1] + s)
    else:
        point = (point[0], point[1] - s)

    points.append(point)

pol = Polygon(points)
print(pol.length + pol.area - pol.length // 2 + 1)
