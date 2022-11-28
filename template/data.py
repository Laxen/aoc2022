import re
from pyhelpers import Grid

def parse_file(input_file, regex):
    pattern = re.compile(regex)

    with open(input_file) as file:
        for line in file:
            search = pattern.search(line.rstrip())

            if search:
                yield search.groups()

def parse_to_grid(input_file):
    matrix = []
    with open(input_file) as file:
        for line in file:
            row = [int(e) for e in line.rstrip()]
            matrix.append(row)
    return Grid.from_2d_list(matrix)

# example =

# input = 
