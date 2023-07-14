"""
|	ArTUI: A TUI drawing program
|
|   # I use git now, so, check that instead!
|	Author:		John D. Reed
|	Start Date:	2023-06-20
|	Last Edit: 2023-06-21
|
|	Notes: Originally intended for learning use only!
"""

import curses
from curses.textpad import Textbox

# Cursor movement keys consts
MOV_LEFT = b"KEY_LEFT"
MOV_DOWN = b"KEY_DOWN"
MOV_UP = b"KEY_UP"
MOV_RIGHT = b"KEY_RIGHT"

QUIT = b"^X"
RESIZE = b"^R"

stdscr = None
scr_maxyx = None # Holds the results of stdscr.getmaxyx()
pad = None
pad_maxyx = None # Holds the results of pad.getmaxyx()
viewport = [0,0] # A list holding the top left corner of the visible pad area
paint_mode = False

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
            # Using getch allows us to "confirm" that the user knows their mistake,
            # Ungetch-ing that input allows us to register it in the textbox for user convinience!
            curses.ungetch(editwin.getch())
            editwin.clear()


def init_pad():
    global pad
    if pad is not None:
        pad.clear()
        refresh_pad()
        
    stdscr.addstr(0,0, f"Input desired height and width of drawing; your screen is {stdscr.getmaxyx()}")
    
    stdscr.addstr(1,0, "Height: ")
    stdscr.refresh()
    height = input_T(int, 1,8)+2 # Add 2 to accommodate border (and future status bars)
    stdscr.addstr(2,0, "Width: ")
    stdscr.refresh()
    width = input_T(int, 2,7)+2 # Same

    pad = curses.newpad(height, width)
    pad.keypad(True)
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

    stdscr.addstr(0,0, "Press ^X to exit; arrow keys to move; ^R to resize pad")
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

def handle_control_char(char):
    """Perform the correct actions for program control characters"""
    # NOTE: It may eventually be better to have a list of all control characters to check if a string is actually a control character
    if char == RESIZE: 
        init_pad()
    else: mov_cursor(char)

def paint(char):
    return

def handle_normal_char(char):
    if paint_mode: paint(char)
    else:
        pad.addch(char)
        mov_cursor(MOV_LEFT) # Addch moves the cursor to the next cell, so we've got to undo that here

def main():
    pad.move(1,1)
    refresh_pad()
    while True:
        char = curses.keyname(pad.getch()) # This essentially does pad.getkey(), except better
        if char == QUIT: return
        elif len(char) > 1: # Special characters like ^R or KEY_LEFT have bytestrings of 2 or longer
            handle_control_char(char)
        else: handle_normal_char(char)


# Call the curses wrapper to safely start the TUI; restores terminal state, etc.
curses.wrapper(init)

