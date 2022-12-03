import sys
from pyhelpers import Parser

def make_data(input_file):
    ret = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.rstrip()
            # ret.append((line[0:int(len(line)/2)], line[int(len(line)/2):]))
            ret.append(line)
    return ret

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

def letter_to_number(letter):
    if letter.isupper():
        return ord(letter) - 64 + 26
    return ord(letter) - 96

def get_common_items(a, b, c):
    ret = []
    for item in a:
        if item in b and item in c and item not in ret:
            ret.append(item)
    return ret

# Part 2
count = 0
for i in range(0, len(data), 3):
    a = data[i]
    b = data[i+1]
    c = data[i+2]
    common = get_common_items(a, b, c)
    for item in common:
        count += letter_to_number(item)

print(count)

# Part 1
# count = 0
# for a, b in data:
#     com = get_common_items(a, b)
#     for c in com:
#         count += letter_to_number(c)
# print(count)
