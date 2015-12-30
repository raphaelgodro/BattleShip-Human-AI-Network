#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Handle the interaction in the grid (onClick) for players of type human
and insert the playing choice or the boat placement choice.
"""
__author__ = "RAGAU72"
__date__ = "2015-12-05"
__teammates__ = "GUCHE29"

class GridInteractions():
    def __init__(self, playerInfo, view):
        """Initialization of the grid interactions attached
        yo a player human."""
        self.playerInfo = playerInfo
        self.view = view
        self.model = view.model
        self.__gridId = playerInfo.PLAYER_GRID
        self.__currentGrid = playerInfo.getGrid(self.__gridId)
        view.screen.onclick(self.__onClick)

    def __onClick(self, x, y):
        """Fired each time a click occurs on the view_window
        Detect if there is a cell first, return None if the click
        was not in the view.

        Will put pending boat cell if the game has not started yet or will
        insert the cell value in the target_cell of the player if the
        game is started."""
        cell = self.view.getCell(x, y, self.__gridId)
        if isinstance(cell, type(None)):
            return
        grid = self.__currentGrid
        on_click_cell_status = grid[cell]
        if cell is not None and on_click_cell_status == grid.EMPTY_CELL:
            playerInfo = self.playerInfo
            # check if the game is not ready
            if not playerInfo.readyToPlay:
                if grid[cell] == grid.EMPTY_CELL:
                    cellState = grid.PENDING_BOAT_CELL
                    grid[cell] = cellState
                    self.view.iconsToDraw.append(cell + (cellState,))
            elif not playerInfo.target_cell:
                playerInfo.target_cell = cell

    def setActionGrid(self, id):
        self.__gridId = id
        self.__currentGrid = self.playerInfo.getGrid(id)



