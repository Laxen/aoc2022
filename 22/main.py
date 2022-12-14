import sys
from pyhelpers import Parser, Grid, Coord
from copy import deepcopy

def make_data(input_file):
    data = Grid(" ", 500, 500)
    width = 0
    height = 0
    with open(input_file, "r") as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.rstrip()):
                data[x, y] = c
                width = max(width, x+1)
            height = max(height, y+1)
    data.width = width
    data.height = height
    return data

if len(sys.argv) > 1:
    print("INPUT\n")
    data = make_data("input")
else:
    print("EXAMPLE\n")
    data = make_data("example")

# -----------------

def get_move_command(path, current_direction):
    steps = ""
    turn = None

    for i, c in enumerate(path):
        if c.isdigit():
            steps += c
        else:
            match c:
                case "R":
                    turn = 1
                case "L":
                    turn = -1

            path = path[i+1:]
            return path, int(steps), turn
    return "", int(steps), turn

def get_loop_coord(pos, direction, face):
    match direction:
        case 0: # Right
            match face:
                case 1:
                    face = 2
                    direction = 0 # Right
                    pos.x = 0
                    pos.y = pos.y
                case 2:
                    face = 5
                    direction = 2 # Left
                    pos.x = side_length - 1
                    pos.y = side_length - 1 - pos.y
                case 3:
                    face = 2
                    direction = 3 # Up
                    pos.x = pos.y
                    pos.y = side_length - 1
                case 4:
                    face = 5
                    direction = 0 # Right
                    pos.x = 0
                    pos.y = pos.y
                case 5:
                    face = 2
                    direction = 2 # Left
                    pos.x = side_length - 1
                    pos.y = side_length - 1 - pos.y
                case 6:
                    face = 5
                    direction = 3 # Up
                    pos.x = pos.y
                    pos.y = side_length - 1
        case 1: # Down
            match face:
                case 1:
                    face = 3
                    direction = 1 # Down
                    pos.x = pos.x
                    pos.y = 0
                case 2:
                    face = 3
                    direction = 2 # Left
                    pos.y = pos.x
                    pos.x = side_length - 1
                case 3:
                    face = 5
                    direction = 1 # Down
                    pos.x = pos.x
                    pos.y = 0
                case 4:
                    face = 6
                    direction = 1 # Down
                    pos.x = pos.x
                    pos.y = 0
                case 5:
                    face = 6
                    direction = 2 # Left
                    pos.y = pos.x
                    pos.x = side_length - 1
                case 6:
                    face = 2
                    direction = 1 # Down
                    pos.x = pos.x
                    pos.y = 0
        case 2: # Left
            match face:
                case 1:
                    face = 4
                    direction = 0 # Right
                    pos.x = 0
                    pos.y = side_length - 1 - pos.y
                case 2:
                    face = 1
                    direction = 2 # Left
                    pos.x = side_length - 1
                    pos.y = pos.y
                case 3:
                    face = 4
                    direction = 1 # Down
                    pos.x = pos.y
                    pos.y = 0
                case 4:
                    face = 1
                    direction = 0 # Right
                    pos.x = 0
                    pos.y = side_length - 1 - pos.y
                case 5:
                    face = 4
                    direction = 2 # Left
                    pos.x = side_length - 1
                    pos.y = pos.y
                case 6:
                    face = 1
                    direction = 1 # Down
                    pos.x = pos.y
                    pos.y = 0
        case 3: # Up
            match face:
                case 1:
                    face = 6
                    direction = 0 # Right
                    pos.y = pos.x
                    pos.x = 0
                case 2:
                    face = 6
                    direction = 3 # Up
                    pos.x = pos.x
                    pos.y = side_length - 1
                case 3:
                    face = 1
                    direction = 3 # Up
                    pos.x = pos.x
                    pos.y = side_length - 1
                case 4:
                    face = 3
                    direction = 0 # Right
                    pos.y = pos.x
                    pos.x = 0
                case 5:
                    face = 3
                    direction = 3 # Up
                    pos.x = pos.x
                    pos.y = side_length - 1
                case 6:
                    face = 4
                    direction = 3 # Up
                    pos.x = pos.x
                    pos.y = side_length - 1

    print("Moving to face", face, "at", pos, "direction", direction)
    return pos, direction, face

def get_loop_coord_ex(pos, direction, face):
    match direction:
        case 0: # Right
            match face:
                case 1:
                    face = 6
                    direction = 2 # Left
                    pos.x = side_length - 1
                    pos.y = side_length - 1 - pos.y
                case 2:
                    face = 3
                    direction = 0 # Right
                    pos.x = 0
                    pos.y = pos.y
                case 3:
                    face = 4
                    direction = 0 # Right
                    pos.x = 0
                    pos.y = pos.y
                case 4:
                    face = 6
                    direction = 1 # Down
                    pos.x = side_length - 1 - pos.y
                    pos.y = 0
                case 5:
                    face = 6
                    direction = 0 # Right
                    pos.x = 0
                    pos.y = pos.y
                case 6:
                    face = 1
                    direction = 2 # Left
                    pos.x = side_length - 1
                    pos.y = side_length - 1 - pos.y
        case 1: # Down
            match face:
                case 1:
                    face = 4
                    direction = 1 # Down
                    pos.x = pos.x
                    pos.y = 0
                case 2:
                    face = 5
                    direction = 3 # Up
                    pos.x = side_length - 1 - pos.x
                    pos.y = side_length - 1
                case 3:
                    face = 5
                    direction = 0 # Right
                    pos.y = side_length - 1 - pos.x
                    pos.x = 0
                case 4:
                    face = 5
                    direction = 1 # Down
                    pos.x = pos.x
                    pos.y = 0
                case 5:
                    face = 2
                    direction = 3 # Up
                    pos.x = side_length - 1 - pos.x
                    pos.y = side_length - 1
                case 6:
                    face = 2
                    direction = 0 # Right
                    pos.y = side_length - 1 - pos.x
                    pos.x = 0
        case 2: # Left
            match face:
                case 1:
                    face = 3
                    direction = 1 # Down
                    pos.x = pos.y
                    pos.y = 0
                case 2:
                    face = 6
                    direction = 3 # Up
                    pos.x = pos.y
                    pos.y = side_length - 1
                case 3:
                    face = 2
                    direction = 2 # Left
                    pos.x = side_length - 1
                    pos.y = pos.y
                case 4:
                    face = 3
                    direction = 2 # Left
                    pos.x = side_length - 1
                    pos.y = pos.y
                case 5:
                    face = 3
                    direction = 3 # Up
                    pos.x = side_length - 1 - pos.y
                    pos.y = side_length - 1
                case 6:
                    face = 5
                    direction = 2 # Left
                    pos.x = side_length - 1
                    pos.y = pos.y
        case 3: # Up
            match face:
                case 1:
                    face = 2
                    direction = 1 # Down
                    pos.x = side_length - 1 - pos.x
                    pos.y = 0
                case 2:
                    face = 1
                    direction = 1 # Down
                    pos.x = side_length - 1 - pos.x
                    pos.y = 0
                case 3:
                    face = 1
                    direction = 0 # Right
                    pos.y = pos.x
                    pos.x = 0
                case 4:
                    face = 1
                    direction = 3 # Up
                    pos.x = pos.x
                    pos.y = side_length - 1
                case 5:
                    face = 4
                    direction = 3 # Up
                    pos.x = pos.x
                    pos.y = side_length - 1
                case 6:
                    face = 4
                    direction = 2 # Left
                    pos.y = side_length - 1 - pos.x
                    pos.x = side_length - 1

    print("Moving to face", face, "at", pos, "direction", direction)
    return pos, direction, face


# path = "0L1"
# path = "10R5L5R10L4R5L5"
path = "47L2R45L20L16L2R33L27R32L12R50L13R23R27L32L27R2R16" \
       "R36L22L13R17L41R5L11R28R4R9R28R44L31L49R31L29R10L4" \
       "L30L46L20R26R37R32L10L39R38L17R5L44R22L36L23L31R38" \
       "R13L36R8R35L33R44R46R13R12L3L19L18L16L16L36L11R20R" \
       "11R7L15R39R46L49L14R32L45R6R13L31L20R40L27L16R7R9R" \
       "41L13L18R47R29L14L10L14L44R35R1R43R37L33L3R45R8L48" \
       "L16L49R33L14R9L15L26L24R1L48L11L18L40L4L27R43R10L5" \
       "L35L41L49R36L24R47L25L9L5R31R48L11L11R5R41R21R8R28" \
       "L37R39L19L5L25L15R4L41L41L14R15R3R47L21L15R2L23L9L" \
       "28L13R24L39L34L34L4R32R36R45R38R43L6L46R30L26R43L4" \
       "9R48R33R7R25R37R7L13L3R38R31L16L9L27R3L36R16R35L33" \
       "R24L30L46R24L37L18R23R15L38L49L39R43R42R39L8L10R23" \
       "L35R44L32L4R4R33R37L41L38R43L26L41L36L28L30L26R37L" \
       "40L31R43L23R22R6R13R38L15L13L25R6L8R14L36R22R48R16" \
       "R29L16L39R11L5R46L46R21L20R2R5R5R31L22L27L29L14L5R" \
       "45R7R45R8R23L27R35L28R25L32L4R3R45R23R3L48L5L6L4L1" \
       "R25L31L20R49R8R37L13R37L22L40L47R18L26R49L32L37R24" \
       "R10L47L47L22R42L11L1R48R32L25R30L14R26R49R29L17R22" \
       "L3R32L41L36L45R13L27L15L50R48L24L31R48R35L5R3L13L4" \
       "4R28R45L35R46L2L12L11L37R37R14L10L13L1L22R7L16L6L3" \
       "0R18R22R3R21L34R45L29L17L36L3L39R11L32L27R29R11L26" \
       "L43L18R28L39L33R7L5R24L19R9L23L11R15L47R20R26L47R4" \
       "R46R8L27R46R37L28L15L44L4L27L32L19L36L47R50L9R47L1" \
       "R26R44L31R10L21L40R43L25L4R14L41L16L15R31R17L40L33" \
       "R25R9L18L46R12L40R31L38L18L15R30L13R49R11L26R34L6L" \
       "49L9R49L49R49R34L36R29R44L45L47L35L25R36L5R17R12L1" \
       "L30R47L45L43R44R50R24R40R27R39R20L4L16L38L26R20L41" \
       "L40R1R5R24L26R29R6L11R50R17L23L15R31L38R22R16L17L7" \
       "R43L4L32L16L7L43R38R34L35R10L45R38L13L15L24R44R11L" \
       "41R44R3R12L2L21L3L47R21R13R39L43R46L17R36R17L31R27" \
       "R30L12L3R4L27L31L41R24L31R48L46L38L28L12R20L39R41L" \
       "43R17L6R17R41L19R34L49L16L41R49R29L49L11R13L9R49R2" \
       "5L48R14R33L38L4L48R4L14R32R31L3L30R4R16L7R7R36L49L" \
       "41R26R34R12L22L2R6R2L22L29L8L37L34L9L2R33R48L10R8R" \
       "9R26R4R8L45R23L6R4L33L11R38R40R35L30L6L44L28R22R19" \
       "L30L38L33L6R11R32R37R50R50R44L34L41R14L17R31L33L34" \
       "R32L22R43L24R37L49R4R29R11R32R24L3R3R19R49R19L40L2" \
       "2R2L8L7L25R16L19L36L10L43R44R12R30R20R11R29L1L7R27" \
       "L24R49R22L47R27L28R6R48L20R38R3L9L1R11R29R32R36R13" \
       "L43L32L5L23L22R3R4R5R38R5L30L3R2L27R21L30R18L28L30" \
       "R27L11L17L21L7L42R10L36L5L28R48R42R32L29L30R32L29R" \
       "10L38L49L10R19R48R21R24L1L23R20L30L44R24L50R5R14L8" \
       "L43R17L44R11L29R9L6R39R42L9L7R47R35R36R5R3L7R22R16" \
       "L38L31R34R45R45L38L37R46L38L7L1L11L5R31L28L25R40R3" \
       "3L3L39R9R2R5L21R4L26R7R23L47L47R16R42R14L46R10R50L" \
       "14L23R37R48R23R25R34R23L14R50R46R27L44R45R35L35R4R" \
       "11R24R12R14R38R32R22R50L26L43R7L40L32R33R22L17R37L" \
       "29R49R44L12R23R21R19R16L17R21R24R36R20R11R32L13L24" \
       "L26R1R2R7L22L35L21L26R30L46R24L46L47L36R43R39L33R2" \
       "L50L25L13R36L42L19L12L43L45L10R28R11L5L49L27R24R2L" \
       "25L6L33R28R18L2L39L30R24R28R48L8L15R39R16R1R34R43R" \
       "45R40L32L23L34L35L13L50L18L39R21L27L27R30L34L16R18" \
       "L29L19R19R25L37R11L1L34R18L17R46R26R19L45L47R25L38" \
       "R13R22L30L14L43R49R7L1L44L20R36R10R5L27R48L9L12R25" \
       "R36L42R12L46R1R1L30R19L3R32R23R29R1R14R30R31L1L15L" \
       "13R36L34R39L16L44R34R34R11L21R23R45L3R19R30L37R4L2" \
       "7R17R23L40L19R21L32L47R49R14L33R18R32L8R40R7R50R2R" \
       "9L15R37L33R7R21L32L1L8L34L24R50R13L9R32R7R34L12R21" \
       "L42L26L3R17L37L7R39R43L15L19R3L7R10L35R34R24R21L8L" \
       "4R49R33R18R46R15L38L18R23L35L12L36R45R5L20L8L49L5R" \
       "21R12L11R8R17R27L16L16L22R29L41L48L18L11L50R34R4L2" \
       "5R14R14R26R36L15L10R12L10L28R45L6L32L38L21L39R16R4" \
       "3L43R29R15L47L2L43L24R39L30L38R24R47R49L43R37L44L4" \
       "6R25R23L37L20L10L4L11L24R23L4R6R42L50L22R36L49L37R" \
       "8R2R49L10L21R50R31L23R30R29R1L35R29L26L9R35R10R41L" \
       "6L30L34R48L50R4L40L20R18R28R23L49L39R10L7L15L48L48" \
       "R45R3R30L35L2L24R43R9L46R5R1R17L13R17R49R22R3L35R4" \
       "6L39L25L40R25L42L24R23R22R32L13L41R11R30L17R44R16L" \
       "6R22R30L45L30L29L16L18L24L10R36R37L42L21R28L41R37R" \
       "47R44R42R15L14R20L4L37R3R7L48L10L38L42L37L13L20L40" \
       "R18L2R5L24L5L45R28R10R2L29R4R10L33R47R37L15R38L27R" \
       "17R24L1R11L30L29L8R13R35R28R19L1R16L37L11R42L31R32" \
       "R28R17R46R13R6R4R15R30R8L46L21R38L17L50R41R2R13L7L" \
       "25R36R25L35L16R32R44R30R32L50L13R7R9L5R6L43L4R16L9" \
       "L31R38R49R27L39L37R14L31R26R49L32L10L23L19L12R35L1" \
       "4L44R37R36L25L18L22R17L40L8R45R49R22R30R28R33R40R5" \
       "0L2L18R16R14L35R1L24R36L44R34L36L25L47L3L2R19L45L1" \
       "9R48R29R38R7R26R50R43R20R1R32R13R44L6R10R17L39L29L" \
       "11L16L4L1R27R14R9L11L28L5L11R11R25R9R28R24L30L21R4" \
       "2L10R10R30R48L25R41L4R49L1R15L5R49R25R25R2R22L22L2" \
       "7R33L17R9L48L49L6R13R36L20R40R37L1R37R13R29R27R49L" \
       "15L15R29L39R5R1R11L2R40R49R1L22R49R7L39R30L34L15L5" \
       "L28R18L7L39L15L13R29R13R11L14R6R29L39R41R47L34R9R3" \
       "6L11R20L36L36L48L16R18R18L23L48L14R32L30R50R38R36L" \
       "47R16R41L37R24R9R11R13L6L18L26L50R44L47R13R14L45R3" \
       "3R44R48L2L18R30L35L48L10R18R36R19R12L27R44R33L40R3" \
       "4R2R3L2L38L1R4R17R32R30L42L11R32L10R25L8R10R1L5L27" \
       "R47R27R50R8L19L7L27L5R28L23L11L34R13R25L48R39L33L4" \
       "5R18R36R44R19R3L37L11L46L40R36L12L15L16L7L16R3R20R" \
       "21L12R20L7L43R49R16L46L38L30R41L47L17L42L2L1R42L48" \
       "L45R3R28R8L18R21R18R32R1L18R37L19R25L26R2L46L20R4R" \
       "26R22L5L40L49L41R3R9R24L3R50R49R48L20R34L22L17L49R" \
       "26L20L6R28R22L44L10L6R48L21L22L27L33R13L32R23R45L3" \
       "3R11R29L50R49L31R34L30R19L10R37L29L8L16R1L21R11R2R" \
       "23L12R8L30L1R15R22L26R31L37L39L25L44R23L50R27L2L33" \
       "R23L5L36L2L9L40R43L19R43L32R4L12R49L25R48L13R13L31" \
       "R5L16L46L46R29L5R23R22R36L13R15R26R43L8L37R30R20L7" \
       "L4R26L33L32R27L40L20L36R39L36L3L19R49R8L28R16R10R4" \
       "0R27R50R36L28R10R8R37R49L28L36L16R44R29L2L31R25L48" \
       "L44L24L21R40R40R24L31L32R37R30R1R22R36L44L23R14R38" \
       "R25R27L5L7R43L45L2R48R30R32R35R48L30L6L31R45R20L14" \
       "R5R25L30R39R9L6L18R6R30L3L15R33R30R14L31R39L11R18L" \
       "35L27R25R26R36R40R43L17R30L14R48R20L40L28R40R6L26L" \
       "36L30R34L31L38L48L12R15R42L36L41R12L44L10L19L4L44R" \
       "23R41R37L45L10R7R48L43R16L43L38R17L49R31L45R29L29L" \
       "43R47R8L3R46R13R39L7R44L37R6L32R33R9R16L5L6R45L42L" \
       "26L19L45R25R4R34R34L19L26L12R21L36L48R27L32L16R34R" \
       "13L15R20L31L27R34R23L15L23R19L27R43R39L13L37L6R7L4" \
       "1L23R36R23R28L6R26L22R32L46R24L27L25R5R43L47R39L46" \
       "R21R45L3L31R36R36L13R33L13R47R27R13L45L22R49R50L10" \
       "R37R18L46L43R50L13R27R33L11L34R26L11R12R5R10L45R43" \
       "L47L25R49L23R50R36R45R11L9L47L36R37R21R36L31L40R33" \
       "R29L15L25R25L9L5R22L50R16L17L32L32L16L8R5R7R38L37"

# pos = Coord(0, 0)
# for c, e in data:
#     if e == ".":
#         pos = Coord(c[0], c[1])
#         break

# 0 = right
# 1 = down
# 2 = left
# 3 = up
direction = 0
face = 1
pos = Coord(0, 0)

# EXAMPLE
# side_length = 4
# faces = dict()
# faces[1] = data[2*side_length:, :side_length]
# faces[2] = data[:side_length, side_length:2*side_length]
# faces[3] = data[side_length:2*side_length, side_length:2*side_length]
# faces[4] = data[2*side_length:3*side_length, side_length:2*side_length]
# faces[5] = data[2*side_length:3*side_length, 2*side_length:3*side_length]
# faces[6] = data[3*side_length:4*side_length, 2*side_length:3*side_length]

# REAL
side_length = 50
faces = dict()
faces[1] = data[side_length:2*side_length, :side_length]
faces[2] = data[2*side_length:, :side_length]
faces[3] = data[side_length:2*side_length, side_length:2*side_length]
faces[4] = data[:side_length, 2*side_length:3*side_length]
faces[5] = data[side_length:2*side_length, 2*side_length:3*side_length]
faces[6] = data[:side_length, 3*side_length:]

for side, grid in faces.items():
    print(side)
    print(grid)

# exit()

print(pos)
faces[face][pos] = "X"
print(faces[face])
faces[face][pos] = "."

while len(path) > 0:
    path, steps, turn = get_move_command(path, direction)
    print("Move", steps, "in direction", direction, "on face", face)

    for s in range(steps):
        newpos = deepcopy(pos)
        newdir = direction
        newface = face

        if direction == 0:
            newpos.x += 1
            if newpos.x > side_length - 1:
                newpos, newdir, newface = get_loop_coord(newpos, direction, face)
        elif direction == 1:
            newpos.y += 1
            if newpos.y > side_length - 1:
                newpos, newdir, newface = get_loop_coord(newpos, direction, face)
        elif direction == 2:
            newpos.x -= 1
            if newpos.x < 0:
                newpos, newdir, newface = get_loop_coord(newpos, direction, face)
        elif direction == 3:
            newpos.y -= 1
            if newpos.y < 0:
                newpos, newdir, newface = get_loop_coord(newpos, direction, face)

        # Revert all movement
        if faces[newface][newpos] == "#":
            newpos = pos
            newdir = direction
            newface = face

        pos = newpos
        direction = newdir
        face = newface


    if turn is not None:
        direction = (direction + turn) % 4

    # print("Face", face, "-", pos)
    # faces[face][pos] = "X"
    # print(faces[face])
    # faces[face][pos] = "."

# row = pos.y + 1
# col = pos.x + 1
# print(row, col, direction)
# print(1000*row + 4*col + direction)

print("Face", face, "-", pos, "direction", direction)
