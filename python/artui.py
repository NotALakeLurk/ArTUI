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
viewport = [0,0] # A list holding the top left and bottom right corners of the viewed portion of pad

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
    stdscr.addstr(0,0, f"Input desired height and width of drawing; your screen is {stdscr.getmaxyx()}")
    
    stdscr.addstr(1,0, "Height: ")
    stdscr.refresh()
    height = input_T(int, 1,8)+2 # Add 2 to accommodate border (and future status bars)
    stdscr.addstr(2,0, "Width: ")
    stdscr.refresh()
    width = input_T(int, 2,7)+2 # Same

    global pad
    pad = curses.newpad(height, width)
    global pad_maxyx # NOTE: This may need to be a list, as it will change with resizing when that's implemented
    pad_maxyx = (height-1, width-1)
    pad.border()
    stdscr.clear()
    stdscr.refresh()
    pad.move(1,1)
    refresh_pad()

def init(initscr):
    global stdscr
    stdscr = initscr
    stdscr.clear()

    global scr_maxyx # Get the screen size to determine the viewport later
    scr_maxyx = tuple(map(lambda n: n-1, stdscr.getmaxyx())) # Subtract 1 from the max y and x because the screen likely doesn't fully show them

    stdscr.addstr(0,0, "Press `q` to exit; h,j,k,l to move; r to resize pad")
    stdscr.getch()
    stdscr.clear()

    init_pad() # Create a new pad of desired size
    main()

def refresh_pad(y=0, x=0):
    """Refresh pad based on the viewport"""
    pad.refresh(*viewport, y,x, *scr_maxyx)
    
def adjust_viewport(pos=None):
    """Adjust the viewport to include the cursor"""
    if pos is None: pos = pad.getyx()
    # Viewport has 2 coordinate pairs that need to stay in sync, so both y or x values must be changed together
    if pos[1] <= viewport[1]+1: # Viewport[1] is the left side of the viewport
        viewport[1] -= 1
    elif pos[0] >= viewport[0]+scr_maxyx[0]: # Viewport[x] + scr_maxyx[x] is the other end of the screen
        viewport[0] += 1
    elif pos[0] <= viewport[0]+1: # Viewport[0] is the top
        viewport[0] -= 1
    elif pos[1] >= viewport[1]+scr_maxyx[1]: 
        viewport[1] += 1

def mov_cursor(char):
    """Move the cursor based on an input character"""
    # Movement
    mov_flag = False
    pos = list(pad.getyx())
    if char == MOV_LEFT and pos[1] > 0+1: # The border+info occupy the edges of the pad (space accounted for) 
        pos[1] -= 1
        mov_flag = True
    elif char == MOV_DOWN and pos[0] < pad_maxyx[0]-1:
        pos[0] += 1
        mov_flag = True
    elif char == MOV_UP and pos[0] > 0+1:
        pos[0] -= 1
        mov_flag = True
    elif char == MOV_RIGHT and pos[1] < pad_maxyx[1]-1:
        pos[1] += 1
        mov_flag = True

    if mov_flag: # Don't do a slow refresh if nothing happened
        pad.move(*pos) 
        adjust_viewport(pos)
        refresh_pad()

def main():
    pad.addstr(pad_maxyx[0], 0, "Test")
    pad.move(1,1)
    refresh_pad()
    while True:
        char = pad.getch()
        # Shortcuts
        if char == ord("q"):
            return
        elif char == ord("r"):
            init_pad()
        else: mov_cursor(char)

# Call the curses wrapper to safely start the TUI; restores terminal state, etc.
curses.wrapper(init)

