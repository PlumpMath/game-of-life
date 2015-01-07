# -*- coding: utf-8 -*-
"""
@author: Patrick K. O'Brien

Conway's Game of Life

Hosted at https://github.com/pkobrien/game-of-life
"""

__version__ = '1.0.0'


import itertools


ACORN = {(0, 2), (1, 0), (1, 2), (3, 1), (4, 2), (5, 2), (6, 2)}
BEACON = {(0, 0), (0, 1), (1, 0), (2, 3), (3, 2), (3, 3)}
BLINKER = {(0, 0), (1, 0), (2, 0)}
GLIDER = {(0, 0), (0, 1), (1, 0), (1, 2), (2, 0)}


def normalize(cells):
    """Return cells offset as close to (0, 0) as possible."""
    x_offset = 0 - min(x for x, y in cells)
    y_offset = 0 - min(y for x, y in cells)
    return offset(cells, x_offset, y_offset)


def offset(cells, x_offset, y_offset):
    """Return a set of cells with x and y offsets applied."""
    return {(x + x_offset, y + y_offset) for x, y in cells}


def sample_population():
    """Return a sample population of cells."""
    return (offset(GLIDER, 0, 0) | 
            offset(BEACON, 2, 10) | 
            offset(BLINKER, 10, 2))


class Grid(object):
    """A toroidal playground and graveyard for cells and their neighbors."""

    def __init__(self, width=1, height=1):
        self.width = max(width, 1)
        self.height = max(height, 1)
        self.generations = 0
        self.living = set()
        self.new_born = set()
        self.new_dead = set()

    def cycle(self):
        """Update grid with the next generation of living cells."""
        if not self.living:
            return
        if self.generations > 1 and not self.new_born and not self.new_dead:
            return
        self.generations += 1
        nextgen = set()
        living = self.living
        recalc = living | set(
            itertools.chain.from_iterable(map(self.neighbors, living)))
        for cell in recalc:
            count = sum((other in living) for other in self.neighbors(cell))
            if count == 3 or (count == 2 and cell in living):
                nextgen.add(cell)
        self.new_born = nextgen.difference(living)
        self.new_dead = living.difference(nextgen)
        self.living = nextgen

    def live_neighbors(self, cell):
        """Generate neighbors of cell that are among the living."""
        for other in (neigh for neigh in self.neighbors(cell) 
                      if neigh in self.living):
            yield other

    def neighbors(self, cell):
        """Generate eight neighboring cells for the given cell."""
        x, y = cell
        # North
        yield x, (y + 1) % self.height
        # Northeast
        yield (x + 1) % self.width, (y + 1) % self.height
        # East
        yield (x + 1) % self.width, y
        # Southeast
        yield (x + 1) % self.width, (y - 1) % self.height
        # South
        yield x, (y - 1) % self.height
        # Southwest
        yield (x - 1) % self.width, (y - 1) % self.height
        # West
        yield (x - 1) % self.width, y
        # Northwest
        yield (x - 1) % self.width, (y + 1) % self.height

    def populate(self, population=None):
        """Seed grid with cells contained in the population set."""
        if population is None:
            population = sample_population()
        self.width = max(self.width, max(x + 1 for x, y in population))
        self.height = max(self.height, max(y + 1 for x, y in population))
        self.generations = 1
        self.living = population
        self.new_born = set()
        self.new_dead = set()
