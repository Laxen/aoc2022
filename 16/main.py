import sys
from pyhelpers import Parser
from pprint import pp
from copy import deepcopy
from time import sleep

class State:
    def __init__(self, current_valve, time, opened_valves, data):
        self.current_valve = current_valve
        self.time = time
        self.opened_valves = opened_valves
        self.pressure = 0

    def is_open(self):
        return self.current_valve in self.opened_valves

    def step(self):
        for valve in self.opened_valves:
            self.pressure += data[valve][0]
        self.time += 1

    def __eq__(self, other):
        return self.current_valve == other.current_valve and self.time == other.time and self.opened_valves == other.opened_valves

    def __hash__(self):
        return hash((self.current_valve, self.time, tuple(self.opened_valves)))

    def __repr__(self):
        return f"State({self.current_valve}, {self.time}, {self.opened_valves}, {self.pressure})"

def make_data(input_file):
    data = dict()
    with open(input_file, "r") as f:
        for valve, rate, valves in Parser.regex(input_file, r"Valve (.*) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)$"):
            # print(valve, rate, valves)
            data[valve] = (int(rate), valves.split(", "))
    return data

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

# def shortest_path(start, end, data):
#     if start == end:
#         return 1
#
#     shortest = 99
#     for next_valve in data[start][1]:
#         s = shortest_path(next_valve, end, data)
#         shortest = min(shortest, s)
#
#
# def simulate(state):


def next_states(state, data):
    next_states = []

    # If the valve is not open and there's a point in opening it, then open it
    if not state.is_open() and data[state.current_valve][0] > 0:
        next_state = deepcopy(state)
        next_state.step()
        next_state.opened_valves.append(state.current_valve)
        # next_state.time += 1
        next_states.append(next_state)

    for next_valve in data[state.current_valve][1]:
        next_state = deepcopy(state)
        next_state.current_valve = next_valve
        next_state.step()
        # next_state.time += 1
        next_states.append(next_state)

    return next_states

pp(data)

init = State("AA", 0, [], data)

states = set()
new_states = set()

states.add(init)

for i in range(30):
    print(i, len(states))
    for state in states:
        # print(state, "-------")

        ns = next_states(state, data)
        new_states.update(ns)
        # for s in ns:
        #     new_states.add(s)

    # print(new_states)
    # print("----------------------------")
    states = new_states
    new_states = set()
    # sleep(1)

max_pressure = 0
for state in states:
    max_pressure = max(max_pressure, state.pressure)
print(max_pressure)
