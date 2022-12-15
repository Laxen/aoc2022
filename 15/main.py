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
            sensors.append(Coord(int(sx), int(sy)))
            beacons.append(Coord(int(bx), int(by)))
            width = max(width, int(sx), int(bx))
            height = max(height, int(sy), int(by))
    return sensors, beacons, width, height

if len(sys.argv) > 1:
    print("INPUT\n")
    sensors, beacons, width, height = make_data("input")
else:
    print("EXAMPLE\n")
    sensors, beacons, width, height = make_data("example")

# -----------------

def manhattan(a, b):
    return abs(a.x-b.x) + abs(a.y-b.y)

def cover(sensor, distance, row):
    row_dist = abs(sensor.y - row)
    if row_dist <= distance:
        diff = distance - row_dist
        return (sensor.x - diff, sensor.x + diff)
    return None

# s = Coord(8,7)
# b = Coord(2,10)
# dist = manhattan(s, b)
# print(cover(s, dist, 16))

def merge_interval(a, b):
    # Case 1, 2, 3 (other to the right of, or inside, self)
    if b[0] >= a[0]:
        # Case 1 (other fully to the right of self, no intersection)
        if b[0] > a[1]:
            return None

        # Case 3 (other fully inside self)
        if b[1] <= a[1]:
            return (a[0], a[1])

        # Case 2 (other partially inside self)
        return (a[0], b[1])
    # Case 4, 5, 6 (self to the right of, or inside, other)
    else:
        # Case 6 (self fully to the right of other, no intersection)
        if a[0] > b[1]:
            return None

        # Case 4 (self fully inside other)
        if a[1] <= b[1]:
            return (b[0], b[1])

        # Case 5 (self partially inside other)
        return (b[0], a[1])

def merge_merge(merged):
    while True:
        if len(merged) == 1:
            return merged[0]

        pp(merged)
        c = merged.pop(0)

        for m in merged:
            new = merge_interval(c, m)
            if new is not None:
                # print("Merged", c, m, "to", new)
                merged.remove(m)
                merged.append(new)
                break
        else:
            merged.append(c)

# row = 2000000

# for row in range(0, 20):
# for row in range(0, 4000000):
row = 2686239
# row = 11
print("Row", row)

covers = []
for sensor, beacon in zip(sensors, beacons):
    dist = manhattan(sensor, beacon)
    cov = cover(sensor, dist, row)
    covers.append(cov)

merged = []
for c in covers:
    if c is None:
        continue

    # print(c)

    for m in merged:
        new = merge_interval(c, m)
        if new is not None:
            # print("Merged", c, m, "to", new)
            merged.remove(m)
            merged.append(new)
            break
    else:
        merged.append(c)

# print(merged)
#
# print("------")

merged = merge_merge(merged)
# print(merged)
print(merged[1] - merged[0])
