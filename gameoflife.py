# -*- coding: utf-8 -*-
"""
@author: Patrick K. O'Brien

Conway's Game of Life

Hosted at https://github.com/pkobrien/game-of-life
"""

__version__ = '1.0.0'


import itertools


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


#==============================================================================
# And now for something completely different. :-)
#==============================================================================


class Farm(object):
    """Testing ground where seeds are grown and measured."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area = width * height
        self.grid = Grid(width, height)
        self.grid_history = []
        self.land = list((x, y) for x in range(width) for y in range(height))
        self.permutations = []
        self.seed_history = []
        self.seeds = []

    def plant(self, max_cells):
        """Plant seeds up to a maximum complexity of max_cells."""
        grid = self.grid
        seed_number = 0
        for n in range(max_cells):
            cell_quantity = n + 1
            for cells in itertools.combinations(self.land, cell_quantity):
                cells = normalize(cells)
                if cells in self.permutations:
                    # Skip permutations whose normalized version has already
                    # been planted and evaluated.
                    continue
                self.permutations.append(cells)
                seed = Seed(seed_number, cells)
                seed_number += 1
                self.seeds.append(seed)
                grid.populate(cells)
                while True:
                    if grid.living in self.grid_history:
                        # The cells in grid.living have been seen before,
                        # either by the current seed or a previous one.
                        # The first seed that produces a cell pattern is
                        # considered the canonical seed and all others are
                        # variants, and therefore less interesting.
                        seed_index = self.grid_history.index(grid.living)
                        other_seed = self.seed_history[seed_index]
                        if seed is not other_seed:
                            seed.variant_of = other_seed
                            other_seed.variations.append(seed)
                        break
                    self.grid_history.append(grid.living)
                    self.seed_history.append(seed)
                    grid.cycle()
                    seed.max_living = max(seed.max_living, len(grid.living))
                seed.generations = grid.generations

    def harvest(self):
        return self.seeds


class Seed(object):
    """A GMO for engineering interesting population sets to seed a grid."""
    
    def __init__(self, number, cells):
        self.number = number
        self.cells = cells
        self.generations = 0
        self.max_living = 0
        self.variant_of = None
        self.variations = []

    @property
    def cell_count(self):
        return len(self.cells)


def sample_harvest(magic_number):
    """Return the results of farming based on the magic_number."""
    magic_number = min(magic_number, 9)
    farm = Farm(width=magic_number, height=magic_number)
    farm.plant(max_cells=magic_number)
    seeds = farm.harvest()
    return seeds


def sample_harvest_9():
    """Return the results of farming a 9x9 grid with up to 9 cells."""
    farm = Farm(width=9, height=9)
    farm.plant(max_cells=9)
    seeds = farm.harvest()
    return seeds
