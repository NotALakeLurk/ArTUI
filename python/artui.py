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
from curses.textpad import Textbox

# Cursor movement keys consts
MOV_LEFT = ord("h")
MOV_DOWN = ord("j")
MOV_UP = ord("k")
MOV_RIGHT = ord("l")

stdscr = None
scr_maxyx = None # Holds the results of stdscr.getmaxyx()
pad = None
pad_maxyx = None # Holds the results of pad.getmaxyx()
viewport = [0,0, None,None] # A list holding the top left and bottom right corners of the viewed portion of pad

def input_T(T, y, x, n=255):
    """Get input of type T from the user"""
    editwin = curses.newwin(1,n, y,x)
    while True:
        box = Textbox(editwin)
        box.edit()
        try:
            return T(box.gather())
        except ValueError:
            editwin.addstr(0,0, f"Enter a(n) {T}")
            editwin.refresh()
            editwin.getch()
            editwin.clear()


def init_pad():
    stdscr.clear()
    stdscr.addstr(0,0, "Input desired height and width of drawing; your screen is {stdscr.getmaxyx()}")
    
    stdscr.addstr(1,0, "Height: ")
    stdscr.refresh()
    height = input_T(int, 1,8)+1 # Add 1 to accomodate border (and future status bars)
    stdscr.addstr(2,0, "Width: ")
    stdscr.refresh()
    width = input_T(int, 2,7)+1 # Same

    global scr_maxyx # Set the viewport size
    if height < scr_maxyx[0]:
        viewport[2] = height
    else: viewport[2] = scr_maxyx
    if width < scr_maxyx[1]:
        viewport[3] = width
    else: viewport[3] = scr_maxyx

    global pad
    pad = curses.newpad(height, width)
    global pad_maxyx # NOTE: This may need to be a list, as it will change with resizing when that's implemented
    pad_maxyx = (height, width)
    pad.border()
    stdscr.clear()
    stdscr.refresh()
    refresh_pad()

def init(initscr):
    global stdscr
    stdscr = initscr
    stdscr.clear()

    global scr_maxyx # Get the screen size to determine the viewport later
    scr_maxyx = tuple(map(lambda n: n-1, stdscr.getmaxyx())) # Subtract 1 from the max y and x because the screen likely doesn't fully show them

    stdscr.addstr(0,0, "Press `q` to exit; h,j,k,l to move")
    stdscr.getch()
    stdscr.clear()

    init_pad() # Create a new pad of desired size
    main()

def refresh_pad(y=0, x=0):
    """Refresh pad based on the viewport"""
    global pad
    pad.refresh(*viewport[0:2], y,x, *viewport[2:4])

def main():
    
    
    # Test the window by waiting for user input and closing
    while True:
        pos = pad.getyx()
        max_pos = pad.getmaxyx()
        char = pad.getch()

        # Shortcuts
        if char == ord("q"):
            return
        # Cursor movement
        elif char == MOV_LEFT and pos[1] > 0: # Restrict cursor to the screen
            pad.move(pos[0], pos[1] - 1)
        elif char == MOV_DOWN and pos[0] < max_pos[0]-1: # max_pos is *just* off the screen @.@
            pad.move(pos[0] + 1, pos[1])
        elif char == MOV_UP and pos[0] > 0:
            pad.move(pos[0] - 1, pos[1])
        elif char == MOV_RIGHT and pos[1] < max_pos[1]-1:
            pad.move(pos[0], pos[1] + 1)
        refresh_pad()

# Call the curses wrapper to safely start the TUI; restores terminal state, etc.
curses.wrapper(init)

