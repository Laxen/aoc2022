import sys
from pyhelpers import Parser
from pprint import pp

def make_data(input_file):
    res = dict()
    with open(input_file, "r") as f:
        for line in f:
            monkey, task = line.rstrip().split(": ")
            if not task.isdigit():
                task = task.split(" ")
            else:
                task = int(task)
            res[monkey] = task
    return res

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

def solve(monkey):
    if isinstance(data[monkey], int):
        return data[monkey]

    operation = data[monkey][1]
    a = solve(data[monkey][0])
    b = solve(data[monkey][2])
    return eval(f"{a}{operation}{b}")

# Part 2 (did it by hand)
data["root"][1] = ","
data["humn"] = 3099532691300

# Part 1
s = solve("root")
print(s)
