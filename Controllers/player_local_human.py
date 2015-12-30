#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Controller class for players of types Human.
"""
__author__ = "RAGAU72"
__date__ = "2015-12-05"
__teammates__ = "GUCHE29"

import numpy as np
import random
import threading
import time

from .player_local import PlayerLocal
from .grid_interactions import GridInteractions


class PlayerHuman(PlayerLocal):

    def __init__(self, playerInfo, view):
        super().__init__(playerInfo, view)
        self.gridInteractions = GridInteractions(playerInfo, view)

    def placeShips(self):
        """Check the boat placement made from the player
        onClick in Grid_Interactions if verify if it fits
        the length of the next boat to place."""
        playerInfo = self.playerInfo
        if playerInfo.readyToPlay:
            return
        boatIndex = len(playerInfo.boats)

        #Verification to check if we are ready to play
        if len(self.model.BOAT_SIZES) == boatIndex:
            print('PLAYER {} READY TO PLAY'.format(self.playerInfo.playerName))
            self.gridInteractions.setActionGrid(
                playerInfo.OPPONENT_GRID)
            playerInfo.readyToPlay = True
            return

        playerGrid = self.playerGrid
        grid_length = self.model.GRID_SIZE

        boat_length = self.model.BOAT_SIZES[boatIndex]

        for i in range(grid_length):
            match = self.getBoatFromSequence(playerGrid.getLine(i), boat_length)
            if match:
                y = match
                self.addBoat(self.rowColToNPCoord([i], match))
                self.__clearPendingCells()
            match = self.getBoatFromSequence(playerGrid.getColumn(i), boat_length)
            if match:
                self.addBoat(self.rowColToNPCoord(match, [i]))
                self.__clearPendingCells()

    def attack(self):
        """attack choice is declared in onClick method of GridInteractions
        # for human players. Return None if no choice made"""
        target_cell = self.playerInfo.target_cell
        if target_cell is not None:
            self.updateCell(self.opponentGrid, target_cell, self.opponentGrid.SENT_SHOT_CELL)
        return target_cell

    def getBoatFromSequence(self, row, boat_length):
        """ Search a number of following cells to confirm the presence of a boat
            in a given number of cells (column or rows of the grid).
            Returns False if no occurence found in this row
        """
        coordinate = []
        increasing_length = 0
        for i in range(len(row)):
            if row[i] == self.playerGrid.PENDING_BOAT_CELL:
                increasing_length += 1
                coordinate.append(i)
            else:
                increasing_length = 0
                coordinate = []
            if increasing_length == boat_length:
                return coordinate
        return False

    def rowColToNPCoord(self, row, col):
        """Gets the coordinate rom a set of rows and columns."""
        boat_coordinates = []
        for y in row:
            for x in col:
                boat_coordinates.append(np.array([x, y]))
        return np.array(boat_coordinates)

    def __clearPendingCells(self):
        """ Clear selected cells that stays after a boat match"""
        playerGrid = self.playerGrid
        pendingCells = playerGrid.getCellsWhere(
            playerGrid.PENDING_BOAT_CELL)
        for cell in pendingCells:
            self.updateCell(playerGrid, cell, playerGrid.EMPTY_CELL)
