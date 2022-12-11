import sys
from pyhelpers import Parser
import re
from pprint import pp

class Monkey:
    def __init__(self):
        self.items = []
        self.operation = ""
        self.test = 0
        self.test_true = -1
        self.test_false = -1
        self.n_inspects = 0

    def action(self, monkeys):
        for item in self.items:
            old = item
            worry = eval(self.operation)
            worry = int(worry / 3)
            if worry % self.test == 0:
                monkeys[self.test_true].items.append(worry)
                # print("Worry", worry, "thrown to", self.test_true)
            else:
                monkeys[self.test_false].items.append(worry)
                # print("Worry", worry, "thrown to", self.test_false)
            self.n_inspects += 1
        self.items = []

    def __repr__(self):
        # return str(self.items) + " " + self.operation + " " + str(self.test) + " " + str(self.test_true) + " " + str(self.test_false)
        return str(self.items)

def make_data(input_file):
    monkeys = []
    m = Monkey()
    with open(input_file, "r") as f:
        for line in f:
            if "Starting" in line:
                items = re.findall(r"\d+", line)
                for i in items:
                    m.items.append(int(i))
            elif "Operation" in line:
                m.operation = line.split("=")[1].strip()
            elif "Test" in line:
                m.test = int(re.findall(r"\d+", line)[0])
            elif "If true" in line:
                m.test_true = int(re.findall(r"\d+", line)[0])
            elif "If false" in line:
                m.test_false = int(re.findall(r"\d+", line)[0])
            elif "Monkey" in line:
                m = Monkey()
            else:
                monkeys.append(m)
        monkeys.append(m)
    return monkeys

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

for _ in range(20):
    for monkey in data:
        monkey.action(data)

res = []
for monkey in data:
    res.append(monkey.n_inspects)
res.sort()
print(res[-1] * res[-2])
