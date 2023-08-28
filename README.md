# ArTUI
ArTUI is a **T**erminal **U**ser **I**nterface primarily for creating text-based art. 
It uses the [Curses](https://docs.python.org/3/library/curses.html) Python library, and may be eventually recreated in C.

## Known Bugs
- Pads where height or width is set to zero will crash ArTUI (Won't fix, why would you need that?)

## Controls (very likely to change)
- Arrow keys for movement
- ^X to quit
- ^R to resize pad (Doesn't clear border)
- ^H to toggle cursor visibility (Useful for screenshots as ArTUI doesn't yet have saving)

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
