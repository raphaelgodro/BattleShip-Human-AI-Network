#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Player model information class.
Has specific and practical boat placement methods.
"""
__author__ = "RAGAU72"
__date__ = "2015-12-05"
__teammates__ = "GUCHE29"

import copy
import numpy as np

from .grid import Grid
import Models

class PlayerInfo():
    HUMAN = 1
    COMPUTER = 2
    NETWORK = 3

    PLAYER_GRID = 0
    OPPONENT_GRID = 1

    def __init__(self, playerName, playerType, isP1):
        """Initialize the information concerning a player
        at the beginning of a game."""
        self.playerName = playerName
        self.playerType = playerType
        self.isP1 = isP1
        self.boats = []
        self.originalBoats = []
        self.estimatedRemainingEnnemyBoats = copy.copy(Models.Model.BOAT_SIZES)
        self.readyToPlay = False
        self.has_boats = True
        # cell target of the player
        self.target_cell = None
        self.grids = [Grid(Models.Model.GRID_SIZE),
            Grid(Models.Model.GRID_SIZE)]

    def removeBoatHitFromEnnemyWhere(self, coordinate):
        """Remove a boat cell that had been touched
        in the boat information arrays. Remove the boat if it has
        no cell anymore and set has_boats to false if there is no
        boat anymore after the removal."""
        index_boat_to_remove = None
        boats = self.boats
        for i in range(len(boats)):
            index_cell_to_remove = None
            for j in range(len(boats[i])):
                if boats[i][j] == coordinate:
                    index_cell_to_remove = j
                    break
            # remove the targeted boat cell into the boat.
            if index_cell_to_remove is not None:
                del boats[i][index_cell_to_remove]

            if len(boats[i]) == 0:
                index_boat_to_remove = i
        # If a boat is empty in the boat list, remove it
        if index_boat_to_remove is not None:
           del boats[index_boat_to_remove]
        self.boats = boats

        # Check if the player still have a boat
        if len(self.boats) == 0:
            self.has_boats = False

        return index_boat_to_remove is not None

    def updateEstimatedRemainingEnnemyBoats(self, coordinate):
        x_directions = np.array([[1, 0], [-1, 0]])
        y_directions = np.array([[0, 1], [0, -1]])
        axis = [x_directions, y_directions]

        axis_boat_lenghts_to_remove = []

        opponent_grid = self.getGrid(self.OPPONENT_GRID)

        max_boat_length = max(self.estimatedRemainingEnnemyBoats)
        for axis_direction in axis:

            boat_length = 1
            for direction in axis_direction:
                for forward_coord in self.genBoatCoords(max_boat_length-1, coordinate+direction, direction):
                    if not opponent_grid.areCoordsValid([forward_coord]) or opponent_grid[forward_coord] != opponent_grid.SENT_TOUCHED_BOAT_CELL:
                        break
                    boat_length += 1

            axis_boat_lenghts_to_remove.append(boat_length)

        boat_lenght_to_remove = max(axis_boat_lenghts_to_remove)
        while boat_lenght_to_remove not in self.estimatedRemainingEnnemyBoats:
            boat_lenght_to_remove -= 1
            if boat_lenght_to_remove <= min(self.estimatedRemainingEnnemyBoats):
                return None

        self.estimatedRemainingEnnemyBoats.remove(boat_lenght_to_remove)
        return boat_lenght_to_remove

    def genBoatCoords(self, boat_length, position, direction):
        return np.array([position + i*direction for i in range(boat_length)])

    def getGrid(self, index):
        """Get the player grid from an index."""
        return self.grids[index]
