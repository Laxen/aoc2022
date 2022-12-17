import sys
from pyhelpers import Parser, Coord, Grid

def make_data(input_file):
    with open(input_file, "r") as f:
        for line in f:
            return line.rstrip()

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

class Shape:
    def __init__(self, shapetype, width_limit):
        self.shapetype = shapetype
        self.width_limit = width_limit

        match shapetype:
            case "-":
                self.coords = [Coord(0, 0),
                               Coord(1, 0),
                               Coord(2, 0),
                               Coord(3, 0)]
            case "+":
                self.coords = [Coord(1, 0),
                               Coord(0, 1),
                               Coord(1, 1),
                               Coord(2, 1),
                               Coord(1, 2)]
            case "J":
                self.coords = [Coord(0, 0),
                               Coord(1, 0),
                               Coord(2, 0),
                               Coord(2, 1),
                               Coord(2, 2)]
            case "I":
                self.coords = [Coord(0, 0),
                               Coord(0, 1),
                               Coord(0, 2),
                               Coord(0, 3)]
            case "O":
                self.coords = [Coord(0, 0),
                               Coord(1, 0),
                               Coord(0, 1),
                               Coord(1, 1)]

    def move(self, direction):
        for coord in self.coords:
            coord.x += direction.x
            coord.y += direction.y

    def undo_move(self, direction):
        for coord in self.coords:
            coord.x -= direction.x
            coord.y -= direction.y

def simulate_rock(shape, jet_index):
    while True:
        jet = data[jet_index]
        jet_index += 1
        if jet_index == len(data):
            jet_index = 0

        if jet == "<":
            move = Coord(-1, 0)
        else:
            move = Coord(1, 0)

        # Move in jet stream
        # print(jet)
        shape.move(move)
        for coord in shape.coords:
            if coord.x < 0 or coord.x >= grid.width:
                shape.undo_move(move)
                break
            if grid[coord] == "#":
                shape.undo_move(move)
                break

        # Move down
        shape.move(Coord(0, -1))
        for coord in shape.coords:
            if grid[coord] == "#":
                shape.undo_move(Coord(0, -1))
                return jet_index

            if coord.y == 0:
                return jet_index

grid = Grid(".", 7, 0)
shapes = ["-", "+", "J", "I", "O"]
jet_index = 0
shape_index = 0

features = dict()

highest_y = 0
actually_highest_y = 0
# iterations = 2022
# feature_step = 100
iterations = 1000000000000
feature_step = 2000
i = 0
while i < iterations:
    shapetype = shapes[shape_index]
    shape_index += 1
    if shape_index == len(shapes):
        shape_index = 0

    grid.height = highest_y + 10

    h = tuple(grid[:, highest_y-20:highest_y+1].flatten())
    if h in features:
        cycle_step = i - feature_step
        n_cycles_to_skip = (iterations - i) // cycle_step
        print("Cycle hit at", i, ", cycle occurs every", cycle_step, "iterations")
        print("We have", iterations - i, "iterations left, so we can skip", n_cycles_to_skip, "cycles and have a final iteration of", i + n_cycles_to_skip * cycle_step)
        highest_y_increase = highest_y - features[h]
        actually_highest_y += highest_y_increase * n_cycles_to_skip
        i += n_cycles_to_skip * cycle_step
        print("Continuing iterations at", i)
    if i == feature_step:
        print("Added feature at", i)
        features[h] = highest_y

    # Create new shape
    shape = Shape(shapetype, grid.width)
    shape.move(Coord(2, highest_y + 4))

    i += 1

    # for coord in shape.coords:
    #     grid[coord] = "@"
    # print(grid)
    # for coord in shape.coords:
    #     grid[coord] = "."

    # Move shape down
    jet_index = simulate_rock(shape, jet_index)

    for coord in shape.coords:
        grid[coord] = "#"
        highest_y = max(highest_y, coord.y)

    # print(grid)
    # print(highest_y)

# print(grid)
print(actually_highest_y + highest_y + 1)
