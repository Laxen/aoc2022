import sys
import re
from pyhelpers import Parser, Grid, Coord
from pprint import pp

def make_data(input_file):
    sensors = []
    beacons = []
    width = 0
    height = 0
    with open(input_file, "r") as f:
        for line in f:
            sx, sy, bx, by = re.findall(r"(-?\d+)", line)
            sensors.append(Coord(int(sx)+2, int(sy)))
            beacons.append(Coord(int(bx)+2, int(by)))
            width = max(width, int(sx), int(bx))
            height = max(height, int(sy), int(by))
    return sensors, beacons, width+2, height

if len(sys.argv) > 1:
    print("INPUT\n")
    sensors, beacons, width, height = make_data("input")
else:
    print("EXAMPLE\n")
    sensors, beacons, width, height = make_data("example")

# -----------------

def manhattan(a, b):
    return abs(a.x-b.x) + abs(a.y-b.y)

grid = Grid(".", width+1, height+1)

for sensor in sensors:
    print(sensor)
    grid[sensor] = "S"

for beacon in beacons:
    grid[beacon] = "B"

# for sensor, beacon in zip(sensors, beacons):
#     dist = manhattan(sensor, beacon)

pp(sensors)
pp(beacons)

print(grid)
