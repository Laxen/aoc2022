import sys
import math
from pyhelpers import Parser, Coord, Grid

def make_data(input_file):
    ret = []
    with open(input_file, "r") as f:
        for line in f:
            d, s = line.rstrip().split(" ")
            ret.append((d, int(s)))
    return ret

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

# class Knot:
#     def __init__(self, x, y, tail):
#         self.x = x
#         self.y = y
#         self.tail = tail
#
#     def step(self, direction):
#         if direction == "R":
#             self.move_to(self.x + 1, self.y)
#         elif direction == "L":
#             self.move_to(self.x - 1, self.y)
#         elif direction == "U":
#             self.move_to(self.x, self.y + 1)
#         elif direction == "D":
#             self.move_to(self.x, self.y - 1)
#
#     def move_to(self, x, y):
#         self.x = x
#         self.y = y
#
#         if self.tail:
#             dx, dy = self - self.tail
#             if dx > 1:
#                 self.tail.move_to(self.x - 1, self.y)
#             elif dx < -1:
#                 self.tail.move_to(self.x + 1, self.y)
#             elif dy > 1:
#                 self.tail.move_to(self.x, self.y - 1)
#             elif dy < -1:
#                 self.tail.move_to(self.x, self.y + 1)
#
#     def __sub__(self, other):
#         return (self.x - other.x, self.y - other.y)
#
# knots = [Knot(0, 0, None)]
#
# for i in range(8):
#     t = Knot(0, 0, knots[i])
#     knots.append(t)
#
# head = Knot(0, 0, knots[-1])
#
# res1 = []
# res2 = []
#
# for direction, steps in data:
#     for i in range(steps):
#         head.step(direction)
#
#         if (knots[-1].x, knots[-1].y) not in res1:
#             res1.append((knots[-1].x, knots[-1].y))
#
#         if (knots[0].x, knots[0].y) not in res2:
#             res2.append((knots[0].x, knots[0].y))
#     print(knots[-6].x, knots[-6].y)
#     #4 0
#     #5 7
#
# print(len(res1))
# print(len(res2))
# exit()

def diff(tail, head):
    n = (head[0] - tail[0], head[1] - tail[1])
    n0 = n[0] / abs(n[0]) if n[0] != 0 else 0
    n1 = n[1] / abs(n[1]) if n[1] != 0 else 0
    return (n0, n1)

def dist(tail, head):
    return math.sqrt((head[0] - tail[0])**2 + (head[1] - tail[1])**2)

def move_tail(tail, head):
    if head == tail:
        return tail

    di = dist(tail, head)
    # print(di)
    if di >= 2:
        d = diff(tail, head)
        if abs(d[0]) > 1:
            tail[0] += d[0]
        if abs(d[1]) > 1:
            tail[1] += d[1]
        return (tail[0] + d[0], tail[1] + d[1])
    else:
        return tail

head = (0, 0)

tails = [(0, 0) for _ in range(9)]
res2 = []

for direction, steps in data:
    for i in range(steps):
        match direction:
            case "R":
                head = (head[0] + 1, head[1])
            case "L":
                head = (head[0] - 1, head[1])
            case "U":
                head = (head[0], head[1] + 1)
            case "D":
                head = (head[0], head[1] - 1)
        tails[0] = move_tail(tails[0], head)
        for i in range(1, len(tails)):
            tails[i] = move_tail(tails[i], tails[i-1])
        if tails[-1] not in res2:
            res2.append(tails[-1])

        cs = [Coord(*head)]
        for tail in tails:
            cs.append(Coord(*tail))
        grid = Grid.from_coords(cs, "H")
        for i, tail in enumerate(tails):
            grid[Coord(*tail)] = i+1

print(len(res2))
