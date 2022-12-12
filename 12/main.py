import sys
from pyhelpers import Parser, Coord, Grid

def make_data(input_file):
    res = []
    s = Coord(0, 0)
    e = Coord(0, 0)
    with open(input_file, "r") as f:
        for y, line in enumerate(f):
            row = []
            for x, c in enumerate(line.rstrip()):
                if c == "S":
                    s = Coord(x, y)
                    row.append(0)
                elif c == "E":
                    e = Coord(x, y)
                    row.append(ord("z") - ord("a"))
                else:
                    row.append(ord(c) - ord("a"))
            res.append(row)
    return res, s, e

if len(sys.argv) > 1:
    print("INPUT\n")
    data, start, end = make_data("input")
else:
    print("EXAMPLE\n")
    data, start, end = make_data("example")

# -----------------

grid = Grid.from_2d_list(data)

# Part 1
path = grid.find_path(start, end)
path.reverse()
print("Part 1", len(path)-1)

# Part 2
# Looking at the input data we can see that the only way to get into the sea of
# c's is to start at any of the a's in the fist column, because they're the
# only a's that neihbors b. So just loop through these to save a bunch of time.
lens = []
for y in range(0, grid.height):
    start = Coord(0, y)
    path = grid.find_path(start, end)
    if path is not None:
        lens.append(len(path) - 1)
print("Part 2", min(lens))
