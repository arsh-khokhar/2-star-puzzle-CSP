To run the program use "python main.py [fc or bt] [heuristic type (0,1,2,or 3)]"

The program will look for all of grid8x8.txt, grid10x10.txt, or grid14x14.txt
in this folder, if any aren't found it will exit.

Upon finding a solution for each grid (or timing out, 10 minutes max per grid)
the program will output to the console which grids it found solutions to, and
the number of nodes checked. Three gui windows will also open up, showing each
of the grids, with stars placed in appropriate cells (if there's a solution).