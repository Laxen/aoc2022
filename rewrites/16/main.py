import sys
from pyhelpers import Parser
import functools
from copy import deepcopy
import itertools
import logging
from pprint import pp

logging.basicConfig(level=logging.ERROR)

def make_data(input_file):
    data = dict()
    with open(input_file, "r") as f:
        for valve, rate, valves in Parser.regex(input_file, r"Valve (.*) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)$"):
            data[valve] = (int(rate), valves.split(", "))
    return data

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")


# -----------------

@functools.cache
def time_to_reach(start, end, path):
    if start == end:
        return 0

    final_path_length = 99
    for neighbor in data[start][1]:
        if neighbor not in path:
            new_path = path + (neighbor)
            time = time_to_reach(neighbor, end, new_path)
            if time is not None:
                final_path_length = min(final_path_length, time + 1)
    return final_path_length

def compute(path, time, pressure, pressure_increase):
    max_pressure = pressure + pressure_increase * (max_time - time)
    paths[path] = max_pressure
    for valve in useful_valves:
        if valve in path:
            continue
        # print(f"Path {path} -> {valve}")
        t = time_to_reach(path[-1], valve, path[-1]) + 1
        if time + t > max_time:
            continue
        pres = compute(path + (valve,), time + t, pressure + pressure_increase * t, pressure_increase + data[valve][0])
        max_pressure = max(max_pressure, pres)
    # print(f"{max_pressure}, {path}")
    return max_pressure

max_time = 26

paths = dict()
useful_valves = [valve for valve in data if data[valve][0] > 0]
compute(("AA",), 0, 0, 0)

paths = dict(sorted(paths.items(), key=lambda x: x[1], reverse=True))

max_pressure = 0
for i, p1 in enumerate(paths):
    # print(max_pressure, i / len(paths))
    for p2 in paths:
        if p1 == p2:
            continue
        n_overlaps = len(set(p1) & set(p2))
        if n_overlaps == 1:
            max_pressure = max(max_pressure, paths[p1] + paths[p2])
            break
print(max_pressure)
