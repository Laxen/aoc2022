import sys
from pyhelpers import Parser

def make_data(input_file):
    ret = []
    with open(input_file, "r") as f:
        for line in f:
            s = line.rstrip().split(" ")
            ret.append(s)
    return ret


if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

class Machine:
    def __init__(self):
        self.clock = 1
        self.x = 1
        self.signal_strength = 0
        self.output = ""

    def draw(self):
        c = (self.clock-1) % 40

        if c == 0:
            self.output += "\n"

        if c >= self.x-1 and c <= self.x+1:
            self.output += "#"
        else:
            self.output += "."

    def calc_signal_strength(self):
        if self.clock in [20, 60, 100, 140, 180, 220]:
            self.signal_strength += self.clock * self.x

    def incr_clock(self):
        self.calc_signal_strength()
        self.draw()
        self.clock += 1

    def noop(self):
        self.incr_clock()

    def addx(self, add):
        self.incr_clock()
        self.incr_clock()

        # After 2 cycles
        self.x += add

m = Machine()

for instr in data:
    match instr[0]:
        case "noop":
            m.noop()
        case "addx":
            m.addx(int(instr[1]))
print("Signal strength:", m.signal_strength)
print(m.output)
