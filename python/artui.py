# Copywright (c) 2023 John D. Reed / NotALakeLurk
# Subject to the MIT License as part of the ArTUI project
# https://opensource.org/license/mit/ https://github.com/NotALakeLurk/ArTUI 

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
viewport = [0,0] # A list holding the top left corner of the visible pad area
painting = False

# UTILS {{{
def input_T(T, y, x, n=255):
    """Get input of type T from the user at location (y,x)"""
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

def getmaxyx(scr):
    # Subtract 1 from the max y and x because the screen likely doesn't fully show them
    return tuple(map(lambda n: n-1, scr.getmaxyx()))

# }}}

# PAD FUNCTIONS {{{
def query_pad_size(stdscr):
    """Query the user about their desired drawing pad size and return the results as a tuple: (y,x)""" 
    querypad = curses.newpad(3, 255)

    # We need scroll if the screen is too small to fit our lines
    scroll_needed = getmaxyx(stdscr)[0] < 3
    viewline = 0 # The uppermost visible line's pad location

    querypad.addstr(0,0, f"Input desired height and width of drawing; your screen is {getmaxyx(stdscr)}")
    viewline += int(scroll_needed) # Add the neccesary scroll to the viewline
    
    querypad.addstr(1,0, "Height: ")
    refresh_pad(stdscr, querypad, (viewline, 0)) # Show the pad from the first char of viewline
    viewline += int(scroll_needed)
    height = input_T(int, 1,8) # Draw the Textbox after the label
    querypad.addstr(1,8, str(height)) # Show the user the height they picked, not needed for width

    querypad.addstr(2,0, "Width: ")
    refresh_pad(stdscr, querypad, (viewline, 0))
    width = input_T(int, 2,7) # Same as before

    querypad.clear()
    refresh_pad(stdscr, querypad, (0,0))

    return (height, width)

def init_pad(stdscr):
    height, width = query_pad_size(stdscr)
    pad = curses.newpad(height, width)

    pad.keypad(True)

    viewport = [0,0]

    refresh_pad(stdscr, pad, viewport)

    return pad, viewport


def refresh_pad(stdscr, pad, viewport, y=0, x=0):
    """Refresh pad based on the viewport"""
    pad.refresh(*viewport, y,x, *getmaxyx(stdscr))

def resize_pad(stdscr, pad, viewport):
    """Resize the pad to a queried size and resolve any viewport conflicts"""
    pad.resize(*query_pad_size(stdscr))

    # Move the viewport if it ends up outside the pad bounds
    pad_maxyx = pad.getmaxyx()
    scr_maxyx = getmaxyx(stdscr)
    for i in range(0,1):
        # NOTE: ArTUI seems like a great place to play with some branchless programming
        # If one of the viewport's edges are outside the bounds,
        # Move it by the difference of the corresponding pad and view edges to bring it back
        if pad_maxyx[i] < (viewport[i]+scr_maxyx[i]):
            viewport[i] -= viewport[i]+scr_maxyx[i] - pad_maxyx[i]

    refresh_pad(stdscr, pad, viewport)

# }}}
    
def init(stdscr):
    stdscr.clear()

    stdscr.addstr(0,0, "Press ^X to exit; arrow keys to move; ^R to resize pad")
    stdscr.getch()
    stdscr.clear()

    pad, viewport = init_pad(stdscr) # Create a new pad of desired size
    main(stdscr, pad, viewport)

def adjust_viewport(stdscr, pad, viewport, pos=None):
    """Adjust the viewport to include the cursor"""
    # TODO: Rework this function to actually work for most cases
    if pos is None: pos = pad.getyx()
    scr_maxyx = getmaxyx(stdscr)
    # Viewport has 2 coordinate pairs that need to stay in sync, so both y or x values must be changed together
    if pos[1] <= viewport[1]: # Viewport[1] is the left side of the viewport
        viewport[1] -= 1
    elif pos[0] >= viewport[0]+scr_maxyx[0]: # Viewport[x] + scr_maxyx[x] is the other end of the screen
        viewport[0] += 1
    elif pos[0] <= viewport[0]: # Viewport[0] is the top
        viewport[0] -= 1
    elif pos[1] >= viewport[1]+scr_maxyx[1]: 
        viewport[1] += 1

def mov_cursor(stdscr, pad, viewport, char):
    """Move the cursor based on an input character"""
    # Movement
    mov_flag = False
    pos = list(pad.getyx())
    pad_maxyx = getmaxyx(pad)
    if char == MOV_LEFT and pos[1] > 0:
        pos[1] -= 1
        mov_flag = True
    elif char == MOV_DOWN and pos[0] < pad_maxyx[0]:
        pos[0] += 1
        mov_flag = True
    elif char == MOV_UP and pos[0] > 0:
        pos[0] -= 1
        mov_flag = True
    elif char == MOV_RIGHT and pos[1] < pad_maxyx[1]:
        pos[1] += 1
        mov_flag = True

    if mov_flag: # Don't do a slow refresh if nothing happened
        pad.move(*pos) 
        adjust_viewport(stdscr, pad, viewport, pos)
        refresh_pad(stdscr, pad, viewport)

def handle_control_char(stdscr, pad, viewport, char):
    """Perform the correct actions for program control characters"""
    # NOTE: It may eventually be better to have a list of all control characters to check if a string is actually a control character
    if char == RESIZE: 
        resize_pad(stdscr, pad, viewport)
    else: mov_cursor(stdscr, pad, viewport, char)

def handle_normal_char(stdscr, pad, viewport, char):
    # TODO: Convert this function to call a tool's function instead of this
    pos = pad.getyx()
    pad.addch(char)
    pad.move(*pos) # Addch moves the cursor to the next cell, so we've got to undo that here
    refresh_pad(stdscr, pad, viewport)

def main(stdscr, pad, viewport):
    while True:
        char = curses.keyname(pad.getch()) # This essentially does pad.getkey(), except better
        if char == QUIT: return
        elif len(char) > 1: # Special characters like ^R or KEY_LEFT have bytestrings of 2 or longer
            handle_control_char(stdscr, pad, viewport, char)
        else: handle_normal_char(stdscr, pad, viewport, char)


# Call the curses wrapper to safely start the TUI; restores terminal state, etc.
curses.wrapper(init)

