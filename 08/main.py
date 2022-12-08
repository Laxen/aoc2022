import sys
from pyhelpers import Parser, Grid

def make_data(input_file):
    lis = []
    with open(input_file, "r") as f:
        for line in f:
            l = []
            for c in line:
                if c != "\n":
                    l.append(int(c))
            lis.append(l)

    return lis

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

vis = [[0 if i != 0 and i != len(data[0])-1 else 1 for i in range(len(data[0]))] for j in range(len(data))]

vis[0] = [1 for i in range(len(vis[0]))]
vis[len(vis) - 1] = [1 for i in range(len(vis[0]))]

def check_left(x, y):
    if x == 0 or y == 0 or x == len(data[0]) - 1 or y == len(data) - 1:
        return 1

    for i in range(0, x):
        if data[y][i] >= data[y][x]:
            return 0
    return 1

def check_right(x, y):
    if x == 0 or y == 0 or x == len(data[0]) - 1 or y == len(data) - 1:
        return 1

    for i in range(x+1, len(data[0])):
        if data[y][i] >= data[y][x]:
            return 0
    return 1

def check_up(x, y):
    if x == 0 or y == 0 or x == len(data[0]) - 1 or y == len(data) - 1:
        return 1

    for i in range(0, y):
        if data[i][x] >= data[y][x]:
            return 0
    return 1

def check_down(x, y):
    if x == 0 or y == 0 or x == len(data[0]) - 1 or y == len(data) - 1:
        return 1

    for i in range(y+1, len(data)):
        if data[i][x] >= data[y][x]:
            return 0
    return 1

for yi in range(0, len(data)):
    y = data[yi]

    for xi in range(0, len(y)):
        x = y[xi]
        left = check_left(xi, yi)
        right = check_right(xi, yi)
        up = check_up(xi, yi)
        down = check_down(xi, yi)
        vis[yi][xi] = left or right or up or down

# for yi in range(1, len(data)-1):
#     y = data[yi]
#
#     for xi in range(1, len(y)-1):
#         left = 1
#         right = 1
#
#         # Left
#         for lxi in range(0, xi):
#             if data[yi][lxi] >= data[yi][xi]:
#                 left = 0
#                 break
#
#         # Right
#         for rxi in range(xi+1, len(y)):
#             print(data[yi][rxi])
#             if data[yi][rxi] >= data[yi][xi]:
#                 right = 0
#                 break
#
#         vis[yi][xi] = left or right

    # # Right
    # for xi in range(len(y)-2, 0):
    #     vis[yi][xi] = 1
    #     for lxi in range(xi, len(y)-1):
    #         if data[yi][lxi] >= data[yi][xi]:
    #             vis[yi][xi] = 0
    #             break


grid = Grid.from_2d_list(vis)
print(grid.count(1))
