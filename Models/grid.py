#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Grid Information Class into the model.
"""
__author__ = "RAGAU72"
__date__ = "2015-12-05"
__teammates__ = "GUCHE29"

import numpy as np

class Grid():
    EMPTY_CELL = 0
    BOAT_CELL = 1

    SENT_SHOT_CELL = 2
    RECEIVED_SHOT_CELL = 3

    SENT_TOUCHED_BOAT_CELL = 4
    RECEIVED_TOUCHED_BOAT_CELL = 5

    SENT_SANK_BOAT_CELL = 7
    RECEIVED_SANK_BOAT_CELL = 8

    SHOULD_NOT_PUT_BOAT_CELL = 8
    PENDING_BOAT_CELL = 9

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size))

    def __getitem__(self, tup):
        x, y = tup
        return int(self.grid[x][y])

    def __setitem__(self, tup, value):
        x, y = tup
        self.grid[x][y] = value

    def getColumn(self, key):
        """Get column in the grid from an index"""
        return self.grid[key]

    def getLine(self, key):
        """Get line in the grid from an index."""
        grid = self.grid.transpose()
        return grid[key]

    def getCellsWhere(self, *keys):
        """Get cells where certaine values (key) are present"""
        cells = []
        grid = self.grid
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                for key in keys:
                    if grid[x][y] == key:
                        cells.append((x, y))
        return cells

    def areCoordsValid(self, cords):
        """Ensure that coordinates are valid according to the grid_size
        of the game."""
        return np.min(cords) >= 0 and np.max(cords) < self.grid_size

    def __str__(self):
        return str(self.grid)