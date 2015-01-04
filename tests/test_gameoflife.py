# -*- coding: utf-8 -*-

import gameoflife as gol


def test_module_version():
    assert len(gol.__version__.split('.')) == 3


def test_grid():
    grid = gol.Grid(0, 0)
    assert grid.width == 1
    assert grid.height == 1
    assert not grid.living
    assert not grid.generations
    cells = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    assert list(grid.neighbors((0, 0))) == cells

def test_sample_population():
    sample = {(0, 0), (0, 1), (1, 0), (1, 2), (2, 0), (2, 10), (2, 11), 
              (3, 10), (4, 13), (5, 12), (5, 13), (10, 2), (11, 2), (12, 2)}
    assert gol.sample_population() == sample
