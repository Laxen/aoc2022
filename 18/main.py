import sys
from pyhelpers import Parser, Coord, Grid
from pprint import pp

def make_data(input_file):
    res = []
    with open(input_file, "r") as f:
        for line in f:
            x, y, z = line.rstrip().split(",")
            res.append(Coord(x, y, z))
    return res

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

def find_caverns(c, parents):
    if parents == None:
        parents = [c]
    else:
        parents.append(c)

    coords = [c]
    for n, e in grid.neighbors(c, diagonal=False).items():
        if e == 1:
            continue
        if n in parents:
            continue

        # Reached the edge, this is not a cavern
        if n.x == 0 or n.y == 0 or n.z == 0:
            return None
        elif n.x == grid.width or n.y == grid.height or n.z == grid.depth:
            return None

        new_coords = find_caverns(n, parents)
        if new_coords is None:
            return None
        coords.extend(new_coords)
    return coords

grid = Grid.from_coords(data, 1)

# Find all pockets and replace them with 1
for c, e in grid:
    if e == 1:
        continue

    coords = find_caverns(c, None)
    if coords is None:
        continue

    for c in coords:
        grid[c] = 1

print(grid)

# Count surface area
count = 0
for c in data:
    neighbors = grid.neighbors(c, False)
    n_neighbors = sum([1 for _, e in neighbors.items() if e == 1])
    area = 6 - n_neighbors
    count += area
print(count)

