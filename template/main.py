import sys
from pyhelpers import Parser

def make_data(input_file):
    pass

if len(sys.argv) > 1:
    print("EXAMPLE\n")
    data = make_data("example")
else:
    print("INPUT\n")
    data = make_data("input")

# -----------------

print(data)
