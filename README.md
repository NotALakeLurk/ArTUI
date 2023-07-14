# ArTUI
ArTUI is a **T**erminal **U**ser **I**nterface primarily for creating text-based art. 
It uses the [Curses](https://docs.python.org/3/library/curses.html) Python library, and may be eventually recreated in C.

## Known Bugs
- Currently crashes when drawing to a pad with zero height and/or width

## Plans
- Version 1 is nearing completion at the time of writing, all that's left to do is color and rewriting some resize code to not delete current art.
	I plan on doing some basic optimization and structuring before working on some QOL features and eventually v2 features.

## Controls (very likely to change)
- Arrow keys for movement
- ^X to quit
- ^R to resize pad (Replaces old pad)

## Features
- v1
	- [x] Character-only text-based visual art (haven't tested outside of ASCII yet, submit an issue or something if it's that important to you)
	- [x] Resizeable pad (doesn't currently keep existing art)
	- [ ] Color
 
- v2
	- [ ] Tools
		- [ ] Fill
		- [ ] Brush size
 	- [ ] Art Vandelay
		- [ ] Importer
		- [ ] Exporter

## Versions
### v0.1 (Versioning start)
#### Added
- ^X to quit
- Arrow key movement
- Character-based art functionality
- Reset and custom size pad
