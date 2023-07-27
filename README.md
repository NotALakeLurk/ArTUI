# ArTUI
ArTUI is a **T**erminal **U**ser **I**nterface primarily for creating text-based art. 
It uses the [Curses](https://docs.python.org/3/library/curses.html) Python library, and may be eventually recreated in C.

## Known Bugs
- Currently crashes when drawing to a pad with zero height and/or width

## Controls (very likely to change)
- Arrow keys for movement
- ^X to quit
- ^R to resize pad (Replaces old pad)

## Features
- v1
	- [x] Character-only text-based visual art (ASCII only currently)
	- [x] Resizeable pad 
	- [ ] Color
 	- [ ] Information bar(s)
 
- v2
	- [ ] Tools
		- [ ] Fill
		- [ ] Brush size
 	- [ ] Art Vandelay
		- [ ] Importer
		- [ ] Exporter
