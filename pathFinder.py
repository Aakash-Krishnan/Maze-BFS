import curses
from curses import wrapper
import time
import queue


maze = [
    ["#", "#", "#", "#", "#", "O", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"],
]


def print_maze(stdscr, maze, path=[]):
    BLUE = curses.color_pair(100)
    RED = curses.color_pair(101)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "X", RED)
            else:
                stdscr.addstr(i, j * 2, value, BLUE)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    # We store the first start_pos to process with that co-ordinate
    # And that array is to map the path.
    # q.put("the position that I'm currently on, [the path]")
    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(stdscr, maze, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end:
            return path

        neighbours = find_neighbours(maze, row, col)

        for neighbour in neighbours:
            if neighbour in visited:
                continue

            r, c = neighbour
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbour]
            q.put((neighbour, new_path))
            visited.add(neighbour)


def find_neighbours(maze, row, col):
    neighbours = []

    if row > 0:  # UP
        neighbours.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neighbours.append((row + 1, col))
    if col > 0:  # LEFT
        neighbours.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbours.append((row, col + 1))
    return neighbours


def main(stdscr):
    # color pattern with id's 100, 101
    curses.init_pair(100, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(101, curses.COLOR_RED, curses.COLOR_BLACK)

    # First we clear the terminal and get the string, refresh the terminal
    # to display the contents and use getch() to wait for the user to enter
    # some key to get back to the terminal.
    stdscr.clear()
    # addstr(row, col, string)
    # stdscr.addstr(5, 0, "Hellowww")
    find_path(maze, stdscr)
    stdscr.getch()


wrapper(main)
