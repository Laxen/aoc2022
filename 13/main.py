import sys
from pyhelpers import Parser
from pprint import pp
from functools import cmp_to_key

def make_data(input_file):
    res = []
    with open(input_file, "r") as f:
        while True:
            p1 = f.readline().rstrip()
            p2 = f.readline().rstrip()
            try:
                res.append(eval(p1))
                res.append(eval(p2))
            except SyntaxError:
                break

            f.readline()
    return res

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

def comp(a, b, indent=""):
    if not isinstance(a, list) and not isinstance(b, list):
        if a == b:
            return 0
        elif a < b:
            print(indent, "Left side is smaller, right order")
            return 1
        else:
            print(indent, "Right side is smaller, NOT right order")
            return -1

    if not isinstance(a, list):
        a = [a]
    if not isinstance(b, list):
        b = [b]

    # for ae, be in zip(a, b):
    for ai, ae in enumerate(a):
        if ai >= len(b):
            print(indent, "Right side ran out of elements")
            return -1
        be = b[ai]
        print(indent, "Compare", ae, "vs", be)
        ok = comp(ae, be, indent + "  ")

        if ok == 0:
            continue
        return ok

    if len(a) < len(b):
        print(indent, "Left side ran out of elements")
        return 1
    else:
        return 0

# idxs = []
# for idx, i in enumerate(range(0, len(data), 2)):
#     print("Pair", idx+1, "---------------")
#     a = data[i]
#     b = data[i+1]
#     print("Compare", a, "vs", b)
#     c = comp(a, b)
#     if c == True:
#         print("RIGHT")
#         idxs.append(idx+1)
#     elif c == False:
#         print("NOT RIGHT")
#     else:
#         print("ERROR")
#         exit()

data.append([[2]])
data.append([[6]])

data = sorted(data, key=cmp_to_key(comp), reverse=True)

pp(data)
i1 = data.index([[2]]) + 1
i2 = data.index([[6]]) + 1
print(i1*i2)

# print(idxs)
# print(sum(idxs))
