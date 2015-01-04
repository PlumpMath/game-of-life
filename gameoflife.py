# -*- coding: utf-8 -*-
"""
@author: Patrick K. O'Brien

Conway's Game of Life

Hosted at https://github.com/pkobrien/game-of-life
"""

__version__ = '1.0.0'


import itertools


class Grid(object):

    def __init__(self, width=1, height=1):
        self.width = max(width, 1)
        self.height = max(height, 1)
        self.living = set()
        self.generations = 0

    def cycle(self):
        """Update grid with the next generation of living cells."""
        self.generations += 1
        nextgen = set()
        living = self.living
        recalc = living | set(
            itertools.chain.from_iterable(map(self.neighbors, living)))
        for cell in recalc:
            count = sum((other in living) for other in self.neighbors(cell))
            if count == 3 or (count == 2 and cell in living):
                nextgen.add(cell)
        self.living = nextgen

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
        """Initialize with the set of cells contained in the population set."""
        if population is None:
            population = sample_population()
        self.width = max(self.width, max(x + 1 for x, y in population))
        self.height = max(self.height, max(y + 1 for x, y in population))
        self.living = population
        self.generations = 1


def sample_population():
    """Return a sample population of cells."""
    beacon = {(0, 0), (0, 1), (1, 0), (2, 3), (3, 2), (3, 3)}
    blinker = {(0, 0), (1, 0), (2, 0)}
    glider = {(0, 0), (0, 1), (1, 0), (1, 2), (2, 0)}
    setup = [(0, 0, glider), (2, 10, beacon), (10, 2, blinker)]
    population = set()
    for x_offset, y_offset, shape in setup:
        for x, y in shape:
            population.add((x + x_offset, y + y_offset))
    return population
