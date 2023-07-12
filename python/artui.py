"""
|	ArTUI: A TUI drawing program
|
|	Author:		John D. Reed
|	Start Date:	2023-06-20
|	Last Edit: 2023-06-21
|
|	Notes: Originally intended for learning use only!
"""

import curses

# Cursor movement keys consts
MOV_LEFT = ord("h")
MOV_DOWN = ord("j")
MOV_UP = ord("k")
MOV_RIGHT = ord("l")

stdscr = None

"""
def get_string(win, y, x, echo=False):
    win.move(y,x)
    curses.echo()
    
    string = ""
"""

def init_pad():
    stdscr.addstr(0,0, "Input desired height and width of drawing")
    
    curses.echo()
    stdscr.addstr(1,0, "Height: ")
    height = stdscr.getstr(1,8)
    stdscr.addstr(2,0, "Width: ")
    width = stdscr.getstr(2,7)
    curses.noecho()
    
    global pad
    pad = curses.newpad(int(height), int(width))

def init():
    stdscr.clear()
    init_pad() # Create a new pad of desired size

def main(initscr):
    global stdscr
    stdscr = initscr
    stdscr.clear()

    init()
    
    """
    stdscr.addstr(0,0, "Press `q` to exit")
    stdscr.addstr(1,0, f"can_change_color: {curses.can_change_color()}")
    """
    
    # Test the window by waiting for user input and closing
    while True:
        pos = stdscr.getyx()
        max_pos = stdscr.getmaxyx()
        char = stdscr.getch()

        # Shortcuts
        if char == ord("q"):
            return
        # Cursor movement
        elif char == MOV_LEFT and pos[1] > 0: # Restrict cursor to the screen
            stdscr.move(pos[0], pos[1] - 1)
        elif char == MOV_DOWN and pos[0] < max_pos[0]-1: # max_pos is *just* off the screen @.@
            stdscr.move(pos[0] + 1, pos[1])
        elif char == MOV_UP and pos[0] > 0:
            stdscr.move(pos[0] - 1, pos[1])
        elif char == MOV_RIGHT and pos[1] < max_pos[1]-1:
            stdscr.move(pos[0], pos[1] + 1)

# Call the curses wrapper to safely start the TUI; restores terminal state, etc.
curses.wrapper(main)

