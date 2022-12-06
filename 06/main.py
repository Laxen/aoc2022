import sys
from pyhelpers import Parser

def make_data(input_file):
    with open(input_file, "r") as f:
        return f.readline().rstrip()

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

def has_repeating_char(string):
    for c in string:
        if string.count(c) > 1:
            return True
    return False

ret = ""
for i in range(len(data)-13):
    if not has_repeating_char(data[i:i+14]):
        print(i+14)
        break

