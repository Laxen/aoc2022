import sys
from pyhelpers import Parser

def conv_to_int(move):
    if move == "A":
        return 0
    elif move == "B":
        return 1
    elif move == "C":
        return 2
    elif move == "X":
        return 0
    elif move == "Y":
        return 1
    elif move == "Z":
        return 2

def score(oppo, me):
    if oppo == me:
        return 3
    elif (me + 1) % 3 == oppo:
        return 0
    elif (me - 1) % 3 == oppo:
        return 6

def get_move(oppo, score):
    if score == 0:
        return (oppo - 1) % 3
    elif score == 1:
        return oppo
    elif score == 2:
        return (oppo + 1) % 3

def make_data(input_file):
    res = []
    with open(input_file, "r") as f:
        for line in f:
            oppo, me = line.split(" ")
            res.append((conv_to_int(oppo), conv_to_int(me.rstrip())))
    return res

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

count = 0
for oppo, s in data:
    me = get_move(oppo, s)
    count += score(oppo, me) + me + 1
print(count)
