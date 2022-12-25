import sys
from pyhelpers import Parser

def make_data(input_file):
    res = []
    with open(input_file, "r") as f:
        for line in f:
            res.append(line.strip())
    return res

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

def snafu_to_dec(snafu):
    dec = 0
    snafu = snafu[::-1]
    for i, c in enumerate(snafu):
        if c == "=":
            c = -2
        elif c == "-":
            c = -1

        dec += int(c) * 5 ** i
    return dec

def dec_to_snafu(dec):
    snafu = ""

    i = 0
    while i >= 0:
        print(dec)
        if dec == 0:
            snafu += "0"*(i+1)
            break

        if dec > sum([2 * 5 ** j for j in range(i+1)]):
            print("Bigger than", sum([2 * 5 ** j for j in range(i+1)]))
            i += 1
        elif dec > sum([1 * 5 ** i] + [2 * 5 ** j for j in range(i)]):
            snafu += "2"
            dec -= 2 * 5 ** i
            i -= 1
        elif dec > sum([0 * 5 ** i] + [2 * 5 ** j for j in range(i)]):
            snafu += "1"
            dec -= 1 * 5 ** i
            i -= 1
        elif dec > sum([-1 * 5 ** i] + [2 * 5 ** j for j in range(i)]):
            snafu += "0"
            i -= 1
        elif dec > sum([-2 * 5 ** i] + [2 * 5 ** j for j in range(i)]):
            snafu += "-"
            dec += 1 * 5 ** i
            i -= 1
        else:
            snafu += "="
            dec += 2 * 5 ** i
            i -= 1

    return snafu

# print(dec_to_snafu(314159265))
# exit()

s = 0
for snafu in data:
    dec = snafu_to_dec(snafu)
    s += dec
    print(f"{snafu} = {dec} = {dec_to_snafu(dec)}")

print(f"Sum: {s}")
print(f"Sum in snafu: {dec_to_snafu(s)}")
