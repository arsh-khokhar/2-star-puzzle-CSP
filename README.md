# A Constraint Satisfaction based 2-Star-Puzzle solver

This solver represents the 2-star puzzle as a Constraint Satisfaction Graph and uses
the backtracking and forward checking algorithms to find a solution. In addition to
the bare-bone algorithms the solver also supports three additional heuristics for
variable ordering

**Find the details and rules about the 2-star puzzle [here](https://www.puzzle-star-battle.com/)**

### Representation

Each star of the puzzle is a Node in the Constraint Satisfaction Graph, and the
constraints (i.e. the rules of the puzzle) are the edges. The initial domains
for each variable is considered to be its block, which in general was proven
to give better performance than initial domains being rows or columns of the
puzzle grid

### Heuristic 1 - Most constrained node

This Heuristic makes the algorithms choose the next unassigned variable as the star which has the least possible values.

### Heuristic 2 - Most constraining node

This Heuristic makes the algorithms choose the next unassigned variable whose assignment reduces the domains of the other unassigned stars the most.

### Heuristic 3 - Hybrid

This Heuristic is a hybrid of both Heuristic 1 and 2, where one of them is chosen randomly at each step.

### Running the program

To run the program use `python main.py [fc or bt] [heuristic type (0,1,2,or 3)]`
The program will look for all of grid8x8.txt, grid10x10.txt, or grid14x14.txt
in this folder, if any aren't found it will exit.

Upon finding a solution for each grid (or timing out, 10 minutes max per grid)
the program will output to the console which grids it found solutions to, and
the number of nodes checked. Three gui windows will also open up, showing each
of the grids, with stars placed in appropriate cells (if there's a solution).

### Grid File format

The grid file should have a name of format gridNxN.txt, where N is the grid size. The file should contain the blocks in the grid as follows:

Block1\t1,2,3,4,5\
Block1\t6,7,8,9,10\
Block3\t11,12,13,14,15\
Block4\t16,17,18,19,20\
Block5\t21,22,23,24,25\
