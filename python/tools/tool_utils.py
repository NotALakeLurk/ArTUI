"""AbstractTool is a Protocol that every ArTUI tool must follow that serves as an interface"""

# from abc import abstractmethod
from Typing import Protocol

from curses import window

class AbstractTool(Protocol):
    main(stdscr: window, pad: window, char: chr): ...
