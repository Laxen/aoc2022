import sys
from pyhelpers import Parser

def make_data(input_file):
    ret = []
    for dat in Parser.regex(input_file, r"move (\d+) from (\d+) to (\d+)"):
        ret.append(dat)
    return ret

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

# def move(number, stack_start, stack_end):
#     for _ in range(number):
#         stack_end.append(stack_start.pop())

def move(number, stack_start, stack_end):
    print(stack_start, stack_end)
    crates = stack_start[-number:]
    stack_end.extend(crates)
    for _ in range(number):
        stack_start.pop()
        print("pop")
    print(stack_start, stack_end)

s1 = ["T", "V", "J", "W", "N", "R", "M", "S"]
s2 = ["V", "C", "P", "Q", "J", "D", "W", "B"]
s3 = ["P", "R", "D", "H", "F", "J", "B"]
s4 = ["D", "N", "M", "B", "P", "R", "F"]
s5 = ["B", "T", "P", "R", "V", "H"]
s6 = ["T", "P", "B", "C"]
s7 = ["L", "P", "R", "J", "B"]
s8 = ["W", "B", "Z", "T", "L", "S", "C", "N"]
s9 = ["G", "S", "L"]

es1 = ["Z", "N"]
es2 = ["M", "C", "D"]
es3 = ["P"]

s1.reverse()
s2.reverse()
s3.reverse()
s4.reverse()
s5.reverse()
s6.reverse()
s7.reverse()
s8.reverse()
s9.reverse()

# es1.reverse()
# es2.reverse()
# es3.reverse()

# INPUT
for number, stack_start, stack_end in data:
    print(number, stack_start, stack_end)
    if stack_start == "1":
        stack_start = s1
        # stack_start = es1
    elif stack_start == "2":
        stack_start = s2
        # stack_start = es2
    elif stack_start == "3":
        stack_start = s3
        # stack_start = es3
    elif stack_start == "4":
        stack_start = s4
    elif stack_start == "5":
        stack_start = s5
    elif stack_start == "6":
        stack_start = s6
    elif stack_start == "7":
        stack_start = s7
    elif stack_start == "8":
        stack_start = s8
    elif stack_start == "9":
        stack_start = s9
    if stack_end == "1":
        stack_end = s1
        # stack_end = es1
    elif stack_end == "2":
        stack_end = s2
        # stack_end = es2
    elif stack_end == "3":
        stack_end = s3
        # stack_end = es3
    elif stack_end == "4":
        stack_end = s4
    elif stack_end == "5":
        stack_end = s5
    elif stack_end == "6":
        stack_end = s6
    elif stack_end == "7":
        stack_end = s7
    elif stack_end == "8":
        stack_end = s8
    elif stack_end == "9":
        stack_end = s9

    # print(number, stack_start, stack_end)
    move(int(number), stack_start, stack_end)

print(s1.pop(), s2.pop(), s3.pop(), s4.pop(), s5.pop(), s6.pop(), s7.pop(), s8.pop(), s9.pop())
# print(es1.pop(), es2.pop(), es3.pop())
