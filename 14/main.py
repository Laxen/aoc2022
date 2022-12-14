import sys
from pyhelpers import Parser, Grid, Coord
from pprint import pp
from time import sleep

def make_data(input_file):
    res = []
    mini = 99999999999
    maxi = -99999999999
    maxy = 0
    with open(input_file, "r") as f:
        for path in f:
            p = []
            for line in path.rstrip().split(" -> "):
                x, y = line.split(",")
                x = int(x)
                y = int(y)

                if x < mini:
                    mini = x
                if x > maxi:
                    maxi = x
                if y > maxy:
                    maxy = y
                p.append((x, y))
            res.append(p)

    return res, mini, maxi, maxy

if len(sys.argv) > 1:
    print("INPUT\n")
    data, mini, maxi, maxy = make_data("input")
else:
    print("EXAMPLE\n")
    data, mini, maxi, maxy = make_data("example")

# -----------------

def simulate_sand(grid, pos):
    if grid[pos] is None:
        return True
    if grid[pos] == ".":
        down = simulate_sand(grid, pos + Coord(0, 1))
        if down:
            return True

        left = simulate_sand(grid, pos + Coord(-1, 1))
        if left:
            return True

        right = simulate_sand(grid, pos + Coord(1, 1))
        if right:
            return True

        grid[pos] = "o"
        return True
    return False

# grid = Grid(".", 60, 200)
grid = Grid(".", 1000, 200)
# grid = Grid(".", 100, 200)
offset = mini - 300

for path in data:
    for i, (x, y) in enumerate(path):
        path[i] = (x - offset, y)

for path in data:
    for i in range(len(path) - 1):
        for x in range(path[i][0], path[i + 1][0] + 1):
            grid[x, path[i][1]] = "#"
        for x in range(path[i][0], path[i + 1][0] - 1, -1):
            grid[x, path[i][1]] = "#"
        for y in range(path[i][1], path[i + 1][1] + 1):
            grid[path[i][0], y] = "#"
        for y in range(path[i][1], path[i + 1][1] - 1, -1):
            grid[path[i][0], y] = "#"

for i in range(grid.width):
    grid[i, maxy+2] = "#"

for i in range(30000):
    print(i)
    simulate_sand(grid, Coord(500 - offset, 0))
    # grid[500 - mini, 0] = "+"
    # print(grid)
    # grid[500 - mini, 0] = "."
    # sleep(1)

print(grid)
print(grid.count("o"))
