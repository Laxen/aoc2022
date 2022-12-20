import sys
from copy import deepcopy
from pyhelpers import Parser

class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

def make_data(input_file):
    res = []
    with open(input_file, "r") as f:
        for line in f:
            num = Number(int(line.rstrip()))
            res.append(num)
    return res

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

order = data.copy()

for n in data:
    n.value *= 811589153

for _ in range(10):
    for n in order:
        i = data.index(n)
        # print(i, n)
        data.remove(n)

        new_i = (i + n.value)%len(data)
        if new_i == 0 and n.value != 0:
            new_i = len(data)

        data.insert(new_i, n)
print(data)

i_zero = 0
for i, n in enumerate(data):
    if n.value == 0:
        i_zero = i
        break

s = 0
for i in range(1000):
    new_i = (i_zero + i) % len(data)
s += data[new_i+1].value

for i in range(2000):
    new_i = (i_zero + i) % len(data)
s += data[new_i+1].value

for i in range(3000):
    new_i = (i_zero + i) % len(data)
s += data[new_i+1].value

print(s)
