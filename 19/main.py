import sys
import re
from pyhelpers import Parser
from copy import deepcopy

class Blueprint:
    def __init__(self, bid, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian):
        self.bid = bid
        self.ore_ore = ore_ore
        self.clay_ore = clay_ore
        self.obsidian_ore = obsidian_ore
        self.obsidian_clay = obsidian_clay
        self.geode_ore = geode_ore
        self.geode_obsidian = geode_obsidian

    def __repr__(self):
        return f"Blueprint({self.bid}, {self.ore_ore}, {self.clay_ore}, {self.obsidian_ore}, {self.obsidian_clay}, {self.geode_ore}, {self.geode_obsidian})"

class State:
    def __init__(self, ore, clay, obsidian, geode, robot_ore, robot_clay, robot_obsidian, robot_geode, blueprint):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode
        self.robot_ore = robot_ore
        self.robot_clay = robot_clay
        self.robot_obsidian = robot_obsidian
        self.robot_geode = robot_geode
        self.blueprint = blueprint

    def collect(self):
        self.ore += self.robot_ore
        self.clay += self.robot_clay
        self.obsidian += self.robot_obsidian
        self.geode += self.robot_geode

    def step(self):
        states = []

        if self.ore >= self.blueprint.ore_ore:
            new_state = deepcopy(self)
            new_state.collect()
            new_state.ore -= self.blueprint.ore_ore
            new_state.robot_ore += 1
            states.append(new_state)
        if self.ore >= self.blueprint.clay_ore:
            new_state = deepcopy(self)
            new_state.collect()
            new_state.ore -= self.blueprint.clay_ore
            new_state.robot_clay += 1
            states.append(new_state)
        if self.ore >= self.blueprint.obsidian_ore and self.clay >= self.blueprint.obsidian_clay:
            new_state = deepcopy(self)
            new_state.collect()
            new_state.ore -= self.blueprint.obsidian_ore
            new_state.clay -= self.blueprint.obsidian_clay
            new_state.robot_obsidian += 1
            states.append(new_state)
        if self.ore >= self.blueprint.geode_ore and self.obsidian >= self.blueprint.geode_obsidian:
            new_state = deepcopy(self)
            new_state.collect()
            new_state.ore -= self.blueprint.geode_ore
            new_state.obsidian -= self.blueprint.geode_obsidian
            new_state.robot_geode += 1
            states.append(new_state)

        new_state = deepcopy(self)
        new_state.collect()
        states.append(new_state)
        return states

    def robot_hash(self):
        return hash((self.robot_ore, self.robot_clay, self.robot_obsidian, self.robot_geode))

    def __repr__(self):
        return f"State(Ore: {self.ore}, Clay: {self.clay}, Obsidian: {self.obsidian}, Geode: {self.geode} " \
               f"ROre: {self.robot_ore}, RClay: {self.robot_clay}, RObsidian: {self.robot_obsidian}, RGeode: {self.robot_geode}, BP: {self.blueprint.bid})"

    def __hash__(self):
        return hash((self.ore, self.clay, self.obsidian, self.geode, self.robot_ore, self.robot_clay, self.robot_obsidian, self.robot_geode, self.blueprint.bid))

    def __eq__(self, other):
        return (self.ore, self.clay, self.obsidian, self.geode, self.robot_ore, self.robot_clay, self.robot_obsidian, self.robot_geode, self.blueprint.bid) == (other.ore, other.clay, other.obsidian, other.geode, other.robot_ore, other.robot_clay, other.robot_obsidian, other.robot_geode, other.blueprint.bid)

    def __ge__(self, other):
        return self.ore >= other.ore and \
               self.clay >= other.clay and \
               self.obsidian >= other.obsidian and \
               self.geode >= other.geode

def make_data(input_file):
    res = []
    with open(input_file, "r") as f:
        for line in f:
            bid, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = re.findall(r"\d+", line.rstrip())
            res.append(Blueprint(int(bid), int(ore_ore), int(clay_ore), int(obsidian_ore), int(obsidian_clay), int(geode_ore), int(geode_obsidian)))
    return res

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

quality_levels = []
for bp in data:
    print("Blueprint", bp.bid, "-------")

    init = State(1, 0, 0, 0, 1, 0, 0, 0, bp)

    states = [init]
    last_states = []

    seen = set()
    best = dict()

    max_geode = 0
    for i in range(24):
        print("Step", i, "(", len(states), ")")

        new_states = []

        for state in states:
            if state in seen:
                continue
            seen.add(state)

            if state.robot_hash() in best:
                if best[state.robot_hash()] >= state:
                    continue
            best[state.robot_hash()] = state

            # No point in hoarding this since it's better to spend
            # if state.ore > 4 and state.clay > 20:
            #     continue

            if i >= 20 and state.geode < max_geode * 0.5:
                continue

            # print(state)
            max_geode = max(max_geode, state.geode)
            new_states += state.step()

        last_states = states
        states = new_states
        # print(max_obsidian)
        # print("------")

    # states = []

    geodes = 0
    for state in last_states:
        geodes = max(geodes, state.geode)
    print(geodes)
    quality_levels.append(geodes * bp.bid)
print("Sum of quality levels:", sum(quality_levels))
