import sys
from enum import Enum


class Dir(Enum):
    N = 1
    E = 2
    S = 3
    W = 4


class Player(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.dir = Dir.N
        self.hist = [(self.row, self.col, self.dir)]


def read_maze(filename="maze_01"):
    file = open(filename, "r")
    text = file.read()
    assert text.count("o") == 1, "Maze should contain exactly 1 starting point."
    assert text.count("x") == 1, "Maze should contain exactly 1 end point."
    maze = text.splitlines()
    return maze


def find_start(maze):
    for i, line in enumerate(maze):
        idx = line.find("o")
        if idx == -1:
            continue
        return i, idx


def is_clear(char):
    if char == "*":
        return False
    return True


def look_north(maze, player):
    row = player.row - 1
    col = player.col
    next = maze[row][col]
    if is_clear(next):
        return row, col, Dir.N
    return -1, -1, Dir.N


def look_east(maze, player):
    row = player.row
    col = player.col + 1
    next = maze[row][col]
    if is_clear(next):
        return row, col, Dir.E
    return -1, -1, Dir.E


def look_south(maze, player):
    row = player.row + 1
    col = player.col
    next = maze[row][col]
    if is_clear(next):
        return row, col, Dir.S
    return -1, -1, Dir.S


def look_west(maze, player):
    row = player.row
    col = player.col - 1
    next = maze[row][col]
    if is_clear(next):
        return row, col, Dir.W
    return -1, -1, Dir.W


def look_forward(maze, player):
    if player.dir == Dir.N:
        return look_north(maze, player)
    elif player.dir == Dir.E:
        return look_east(maze, player)
    elif player.dir == Dir.S:
        return look_south(maze, player)
    else:
        return look_west(maze, player)


def look_right(maze, player):
    if player.dir == Dir.N:
        return look_east(maze, player)
    elif player.dir == Dir.E:
        return look_south(maze, player)
    elif player.dir == Dir.S:
        return look_west(maze, player)
    else:
        return look_north(maze, player)


def look_left(maze, player):
    if player.dir == Dir.N:
        return look_west(maze, player)
    elif player.dir == Dir.E:
        return look_north(maze, player)
    elif player.dir == Dir.S:
        return look_east(maze, player)
    else:
        return look_south(maze, player)


def look_back(maze, player):
    if player.dir == Dir.N:
        return player.row + 1, player.col, Dir.S
    elif player.dir == Dir.E:
        return player.row, player.col - 1, Dir.W
    elif player.dir == Dir.S:
        return player.row - 1, player.col, Dir.N
    else:
        return player.row, player.col + 1, Dir.E


def find_path(maze, player):
    row, col, dir = look_forward(maze, player)
    if row != -1:
        return row, col, dir
    row, col, dir = look_right(maze, player)
    if row != -1:
        return row, col, dir
    row, col, dir = look_left(maze, player)
    if row != -1:
        return row, col, dir
    return look_back(maze, player)


def navigate_maze(maze, player):
    while maze[player.row][player.col] != "x":
        player.row, player.col, player.dir = find_path(maze, player)
        print("Current position: {}, {}".format(player.row, player.col))
        print("Current direction: {}".format(player.dir))
        if (player.row, player.col, player.dir) in player.hist:
            # If we're in the same place facing the same direction as we've
            # been at some point in the past and we still haven't found the
            # exit, we can only end up in an infinite loop.
            return False
        player.hist.append((player.row, player.col, player.dir))
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        maze = read_maze(sys.argv[1])
    else:
        maze = read_maze()
    row, col = find_start(maze)
    player = Player(row, col)
    if navigate_maze(maze, player):
        print("Successfully navigated the maze!")
    else:
        print("Maze cannot be solved using the current algorithm.")
