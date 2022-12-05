import sys
from pyhelpers import Parser

def make_data(input_file):
    ret = []
    with open(input_file, "r") as f:
        for a in Parser.regex(input_file, r"(\d+)-(\d+),(\d+)-(\d+)"):
            ret.append(a)
    return ret

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

def part1():
    count = 0
    for l in data:
        a = int(l[0])
        b = int(l[1])
        c = int(l[2])
        d = int(l[3])

        if a >= c:
            if b <= d:
                count += 1
                continue
        if c >= a:
            if d <= b:
                count += 1
    print(count)

def part2():
    count = 0
    for l in data:
        a = int(l[0])
        b = int(l[1])
        c = int(l[2])
        d = int(l[3])

        if a >= c and a <= d:
            count += 1
            continue
        if c >= a and c <= b:
            count += 1
    print(count)

part1()
