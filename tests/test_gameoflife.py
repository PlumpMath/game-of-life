# -*- coding: utf-8 -*-

import gameoflife as gol


def test_module_version():
    assert len(gol.__version__.split('.')) == 3


def test_module_constants():
    assert len(gol.ACORN) == 7
    assert len(gol.BEACON) == 6
    assert len(gol.BLINKER) == 3
    assert len(gol.GLIDER) == 5


def test_grid():
    grid = gol.Grid(0, 0)
    assert grid.width == 1
    assert grid.height == 1
    assert not grid.generations
    assert not grid.living
    assert not grid.new_born
    assert not grid.new_dead
    cells = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    assert list(grid.neighbors((0, 0))) == cells


def test_offset():
    assert gol.offset(gol.GLIDER, 0, 0) == {(0, 0), (0, 1), (1, 0), (1, 2), (2, 0)}
    assert gol.offset(gol.BEACON, 2, 10) == {(2, 10), (2, 11), (3, 10), (4, 13), (5, 12), (5, 13)}
    assert gol.offset(gol.BLINKER, 10, 2) == {(10, 2), (11, 2), (12, 2)}
    assert gol.offset(gol.offset(gol.BEACON, 2, 10), -2, -10) == gol.BEACON


def test_sample_population():
    sample = {(0, 0), (0, 1), (1, 0), (1, 2), (2, 0), (2, 10), (2, 11), 
              (3, 10), (4, 13), (5, 12), (5, 13), (10, 2), (11, 2), (12, 2)}
    assert gol.sample_population() == sample
