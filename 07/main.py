import sys
from pyhelpers import Parser
import re

def make_data(input_file):
    sizes = dict()
    directories = []
    with open(input_file, "r") as f:
        directory = ""
        for line in f:
            if "$ cd" in line:
                directory = line.split("$ cd ")[1].strip()
                if directory != "..":
                    directories.append(directory)
                    sizes["/".join(directories)] = 0
                else:
                    directories.pop()
            else:
                r = re.search(r"^(\d+) ", line)
                if r:
                    s = r.group(1)
                    for i, d in enumerate(directories):
                        sizes["/".join(directories[:i+1])] += int(s)
    return sizes


if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

print(data)

# Part 1
# count = 0
# for key, value in data.items():
#     print(key, value)
#     if value <= 100000:
#         count += value
# print(count)

# Part 2
freespace = 70000000 - data["/"]
delspace = 30000000 - freespace

dels = []
for key, value in data.items():
    if value >= delspace:
        dels.append(value)
print(min(dels))
