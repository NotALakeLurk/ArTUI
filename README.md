# ArTUI
ArTUI is a **T**erminal **U**ser **I**nterface primarily for creating text-based art. 
It uses the [Curses](https://docs.python.org/3/library/curses.html) Python library, and may be eventually recreated in C.

## Known Bugs
- Crashes when writing to a pad with zero height (Out of bounds addch())
- Crashes when writing to the bottom right corner of a pad (addch() pushes the cursor to the right,
    in the case that there is no space, the cursor is wrapped to the next line.
    at the bottom-right corner, this results in an out-of-bounds cursor.

## Controls (very likely to change)
- Arrow keys for movement
- ^X to quit
- ^R to resize pad (Replaces old pad)

## Features

- [x] Character-only text-based visual art (ASCII only currently)
- [x] Resizeable pad 
- [ ] Color
 - [ ] Information bar(s)
- [ ] Tools
	- [ ] Fill
	- [ ] Brush size
 - [ ] Art Vandelay
	- [ ] Importer
	- [ ] Exporter
