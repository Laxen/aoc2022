import sys
from pyhelpers import Parser

def make_data(input_file):
    cals = []
    with open(input_file, "r") as f:
        cal = 0
        for line in f:
            if line == "\n":
                cals.append(cal)
                cal = 0
                continue
            cal += int(line)
    cals.append(cal)
    return cals

if len(sys.argv) > 1:
    print("EXAMPLE\n")
    data = make_data("example")
else:
    print("INPUT\n")
    data = make_data("input")

# -----------------

list.sort(data, reverse=True)
print(sum(data[:3]))
