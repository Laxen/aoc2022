import sys
from pyhelpers import Parser, Grid, Coord
from copy import deepcopy

def make_data(input_file):
    res = []
    with open(input_file, "r") as f:
        for line in f:
            res.append(line.strip())
    return Grid.from_2d_list(res)

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

class Blizzard:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def __repr__(self):
        return f"Blizzard({self.pos}, {self.direction})"

def step():
    new_blizzards = dict()

    for _, bzs in blizzards.items():
        for blizzard in bzs:
            newpos = blizzard.pos + blizzard.direction
            if data[newpos] == "#":
                if blizzard.direction == Coord(1, 0):
                    newpos = Coord(1, blizzard.pos.y)
                elif blizzard.direction == Coord(-1, 0):
                    newpos = Coord(data.width - 2, blizzard.pos.y)
                elif blizzard.direction == Coord(0, 1):
                    newpos = Coord(blizzard.pos.x, 1)
                elif blizzard.direction == Coord(0, -1):
                    newpos = Coord(blizzard.pos.x, data.height - 2)
            blizzard.pos = newpos

            if newpos in new_blizzards:
                new_blizzards[newpos].append(blizzard)
            else:
                new_blizzards[newpos] = [blizzard]
    return new_blizzards

def visualize():
    grid = deepcopy(data)
    for _, bzs in blizzards.items():
        for blizzard in bzs:
            if blizzard.direction == Coord(1, 0):
                grid[blizzard.pos] = ">"
            elif blizzard.direction == Coord(-1, 0):
                grid[blizzard.pos] = "<"
            elif blizzard.direction == Coord(0, 1):
                grid[blizzard.pos] = "v"
            elif blizzard.direction == Coord(0, -1):
                grid[blizzard.pos] = "^"
    print(grid)

def move():
    new_positions = set()
    for pos in positions:
        for direction in [Coord(1, 0), Coord(-1, 0), Coord(0, 1), Coord(0, -1), Coord(0, 0)]:
            newpos = pos + direction

            if newpos.x < 1 or newpos.x > data.width - 2 or (newpos.y < 1 and newpos.x != 1) or (newpos.y > data.height - 2 and newpos.x != data.width - 2):
                continue

            if newpos in blizzards:
                continue

            new_positions.add(newpos)
    return new_positions

# Make blizzard list
blizzards = dict()
for c, e in data:
    if e == ">":
        blizzards[c] = [Blizzard(c, Coord(1, 0))]
        data[c] = "."
    elif e == "<":
        blizzards[c] = [Blizzard(c, Coord(-1, 0))]
        data[c] = "."
    elif e == "^":
        blizzards[c] = [Blizzard(c, Coord(0, -1))]
        data[c] = "."
    elif e == "v":
        blizzards[c] = [Blizzard(c, Coord(0, 1))]
        data[c] = "."

start = Coord(1, 0)
positions = set([start])

visualize()
state = 0
trip_time = 0
total_time = 0
for i in range(10000):
    blizzards = step()
    positions = move()
    # visualize()
    # print(positions)

    for pos in positions:
        if pos == Coord(data.width - 2, data.height - 1) and (state == 0 or state == 2):
            print("Reached goal", trip_time + 1)
            positions = set([pos])
            state += 1
            total_time += trip_time + 1
            trip_time = -1
            break
        elif pos == Coord(1, 0) and state == 1:
            print("Reached start", trip_time + 1)
            positions = set([start])
            state += 1
            total_time += trip_time + 1
            trip_time = -1
            break

    if state == 3:
        break

    trip_time += 1
print(total_time)
