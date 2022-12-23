import sys
from pyhelpers import Parser, Grid, Coord
from copy import deepcopy

pad_len = 200

def make_data(input_file):
    res = []
    with open(input_file, "r") as f:
        for line in f:
            padding = "." * pad_len
            res.append(padding + line.rstrip() + padding)

    padding = "." * len(res[0])
    for _ in range(pad_len):
        res.insert(0, padding)
        res.append(padding)
    return Grid.from_2d_list(res)

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

# Round 1
def round1():
    proposed_moves = dict()
    for c, e in data:
        if e == "#":
            neighbors = data.neighbors(c)

            for n in neighbors.values():
                if n == "#":
                    # Found a neighbor, this elf should move
                    break
            else:
                # No neighbors, this elf should NOT move
                continue

            # Find the first neighbor in the proposed direction
            move_dir = None
            for d in dir_order:
                if d in ["N", "S"]:
                    for x in range(-1, 2, 1):
                        dir_coord = c + dir_to_coord[d] + Coord(x, 0)
                        if neighbors[dir_coord] == "#":
                            # Can't move here, so break out to next dir
                            break
                    else:
                        move_dir = d
                        break
                else:
                    for y in range(-1, 2, 1):
                        dir_coord = c + dir_to_coord[d] + Coord(0, y)
                        if neighbors[dir_coord] == "#":
                            # Can't move here, so break out to next dir
                            break
                    else:
                        move_dir = d
                        break

            if move_dir is not None:
                # print(c, "Will move", move_dir)
                # If another elf is already moving here, none will move
                if c + dir_to_coord[move_dir] in proposed_moves:
                    proposed_moves[c + dir_to_coord[move_dir]] = None
                else:
                    proposed_moves[c + dir_to_coord[move_dir]] = c

    return proposed_moves

def round2(proposed_moves):
    moved = False
    for c, e in proposed_moves.items():
        if e is not None:
            data[c] = "#"
            data[e] = "."
            moved = True
    return moved

def count_ground_tiles():
    xmin = 9999999
    xmax = 0
    ymin = 9999999
    ymax = 0

    for c, e in data:
        if e == "#":
            xmin = min(xmin, c.x)
            xmax = max(xmax, c.x)
            ymin = min(ymin, c.y)
            ymax = max(ymax, c.y)

    return data[xmin:xmax+1, ymin:ymax+1].count(".")

dir_order = ["N", "S", "W", "E"]
dir_to_coord = {"N": Coord(0, -1), "S": Coord(0, 1), "W": Coord(-1, 0), "E": Coord(1, 0)}

print("START")
i = 0
while True:
    print(i)
    i += 1

    proposed_moves = round1()
    moved = round2(proposed_moves)
    dir_order.append(dir_order.pop(0))

    if not moved:
        break

print(count_ground_tiles())
