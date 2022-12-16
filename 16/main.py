import sys
from pyhelpers import Parser
from pprint import pp
from copy import deepcopy
from time import sleep

class State:
    def __init__(self, current_valve, elephant_valve, time, opened_valves, data):
        self.current_valve = current_valve
        self.elephant_valve = elephant_valve
        self.opened_valves = opened_valves
        self.pressure = 0

    def is_human_open(self):
        return self.current_valve in self.opened_valves

    def is_elephant_open(self):
        return self.elephant_valve in self.opened_valves

    def step(self):
        for valve in self.opened_valves:
            self.pressure += data[valve][0]

    @property
    def name(self):
        names = [self.current_valve, self.elephant_valve]
        return "".join(sorted(names))

    def __eq__(self, other):
        return (self.current_valve == other.current_valve or self.current_valve == other.elephant_valve) and \
               (self.elephant_valve == other.elephant_valve or self.elephant_valve == other.current_valve) and \
               sorted(self.opened_valves) == sorted(other.opened_valves)

    def __hash__(self):
        return hash((tuple(sorted((self.current_valve, self.elephant_valve))), tuple(sorted(self.opened_valves))))

    def __repr__(self):
        return f"State({self.current_valve}, {self.elephant_valve}, {self.opened_valves}, {self.pressure})"

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

def next_states(state, data):
    next_states = []

    # Human opens
    if not state.is_human_open() and data[state.current_valve][0] > 0:
        # Elephant opens
        if not state.is_elephant_open() and data[state.elephant_valve][0] > 0 and state.elephant_valve != state.current_valve:
            next_state = deepcopy(state)
            next_state.step()
            next_state.opened_valves.append(state.current_valve)
            next_state.opened_valves.append(state.elephant_valve)
            next_states.append(next_state)

        # Elephant moves
        for next_elephant_valve in data[state.elephant_valve][1]:
            next_state = deepcopy(state)
            next_state.step()
            next_state.opened_valves.append(state.current_valve)
            next_state.elephant_valve = next_elephant_valve
            next_states.append(next_state)

    # Human moves
    for next_valve in data[state.current_valve][1]:
        # Elephant opens
        if not state.is_elephant_open() and data[state.elephant_valve][0] > 0:
            next_state = deepcopy(state)
            next_state.step()
            next_state.current_valve = next_valve
            next_state.opened_valves.append(state.elephant_valve)
            next_states.append(next_state)

        # Elephant moves
        for next_elephant_valve in data[state.elephant_valve][1]:
            next_state = deepcopy(state)
            next_state.step()
            next_state.current_valve = next_valve
            next_state.elephant_valve = next_elephant_valve
            next_states.append(next_state)

    return next_states

def debug(*string):
    # print(*string)
    pass

pp(data)

init = State("AA", "AA", 0, [], data)

states = list()
new_states = dict()

care_states = dict()
best_states = dict()

states.append(init)

max_pressure = 0

for i in range(26):
    print(i, len(states))
    for state in states:
        ns = next_states(state, data)
        for n in ns:
            debug("Looking at", n)
            if n in care_states:
                if care_states[n] >= n.pressure:
                    debug("    Better state already exists, discarding")
                    continue
                # debug(n, "improved", care_states[n])
                care_states[n] = n.pressure
            else:
                # debug(n, "New state found, keeping")
                care_states[n] = n.pressure

            if i >= 10:
                if len(n.opened_valves) < 4 or n.pressure < max_pressure * 0.9:
                    continue

            if n.name in best_states:
                best_state = best_states[n.name]
                # If best state has all open valves that new state has, and has higher pressure, discard new state
                if set(best_state.opened_valves).issuperset(set(n.opened_valves)) and best_state.pressure >= n.pressure:
                    debug("    Best state is better", best_state)
                    continue
                # If new state has all open valves that best state has, and has higher pressure, replace it
                elif set(n.opened_valves).issuperset(set(best_state.opened_valves)) and n.pressure >= best_state.pressure:
                    debug("    This is the best state!")
                    best_states[n.name] = n
            else:
                debug("    No best state, adding")
                best_states[n.name] = n
            debug("    Adding", n)
            new_states[n] = n

    states = list(new_states.values())
    new_states = dict()
    # pp(states)
    debug("----------------------------")

    for state in states:
        max_pressure = max(max_pressure, state.pressure)
    print(max_pressure)
    # sleep(1)

print("DONE")

for state in states:
    max_pressure = max(max_pressure, state.pressure)
print(max_pressure)
