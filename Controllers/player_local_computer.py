#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Controller class for computer of type AI.
"""
__author__ = "GUCHE29"
__date__ = "2015-12-05"
__teammates__ = "RAGAU72"

import abc
import math
import random
import time
import numpy as np

from .player_local import PlayerLocal


class PlayerComputer(PlayerLocal):

    def __init__(self, playerInfo, view):
        super().__init__(playerInfo, view)

    def attack(self):
        """Gets the target cell of the next attack from
        class submethods and update the player's grid accordingly."""
        target_cell = self.playerInfo.target_cell
        if target_cell is None:

            target_cell = self.__bestNextPlaceToShoot()

            self.opponentGrid[target_cell] = self.opponentGrid.SENT_SHOT_CELL
            self.updateCell(self.opponentGrid, target_cell, self.opponentGrid.SENT_SHOT_CELL)
            self.playerInfo.target_cell = target_cell
        return target_cell

    def __bestNextPlaceToShoot(self):
        """ Will find a good new place to shoot.
        """
        grid_length = self.model.GRID_SIZE
        remaining_empty_cells = self.opponentGrid.getCellsWhere(self.opponentGrid.EMPTY_CELL)
        touched_boat_cells = self.opponentGrid.getCellsWhere(self.opponentGrid.SENT_TOUCHED_BOAT_CELL)

        # 4 unit directions, randomly ordered:
        every_directions = np.array(random.sample([[1, 0], [0, 1], [-1, 0], [0, -1]], 4))

        rand_mean = len(remaining_empty_cells)
        proba_grid = self.__get2DSigGrid(grid_length, 10*grid_length/rand_mean)

        for position in touched_boat_cells:
            if self.__isTouchedCellSingle(position, every_directions):
                for direction in every_directions:
                    potential_shoot_pos = position + direction
                    can_shoot_there = (
                        self.opponentGrid.areCoordsValid(potential_shoot_pos) and
                        tuple(potential_shoot_pos) in remaining_empty_cells
                    )
                    if can_shoot_there:
                        proba_grid[potential_shoot_pos[0], potential_shoot_pos[1]] += 100

        for boat_length in self.playerInfo.estimatedRemainingEnnemyBoats:
            for direction in every_directions:
                for position in touched_boat_cells:

                    forward_cell_coord = position + direction
                    opposite_cell_coord = position - direction
                    boat_cords = self.playerInfo.genBoatCoords(int(boat_length/2), forward_cell_coord, direction)

                    try:
                        is_forward_cell_alligned_on_a_line = self.opponentGrid[opposite_cell_coord] == self.opponentGrid.SENT_TOUCHED_BOAT_CELL and (
                            self.opponentGrid[forward_cell_coord] == self.opponentGrid.EMPTY_CELL
                        )
                    except IndexError:
                        is_forward_cell_alligned_on_a_line = False
                    if is_forward_cell_alligned_on_a_line:
                        proba_grid[forward_cell_coord[0]][forward_cell_coord[1]] += 100

                    can_place_boat_here = self.__canPlaceBoatHere(
                        self.opponentGrid, boat_cords
                    )
                    can_place_boat_here_but_shot = self.__canPlaceBoatHere(
                        self.opponentGrid, boat_cords, accept_shot_cells=True
                    )
                    if can_place_boat_here or can_place_boat_here_but_shot:
                        for coord in boat_cords:
                            proba_grid[coord[0]][coord[1]] += (
                                3*int(
                                    can_place_boat_here)
                                + random.randint(1, 2)*int(
                                    can_place_boat_here_but_shot and list(coord) not in np.array(touched_boat_cells).tolist())
                            )

                for i in range(grid_length):
                    for j in range(grid_length):
                        position = np.array([i, j])


                        boat_cords = self.playerInfo.genBoatCoords(boat_length, position, direction)

                        can_place_boat_here = self.__canPlaceBoatHere(
                            self.opponentGrid, boat_cords
                        )

                        if can_place_boat_here:
                            for coord in boat_cords:
                                proba_grid[coord[0]][coord[1]] += 1

        shot_coord = np.unravel_index(np.argmax(proba_grid), proba_grid.shape)

        if shot_coord not in remaining_empty_cells:
            return self.__bestNextPlaceToShoot()
        return shot_coord

    def __isTouchedCellSingle(self, position, every_directions):
        is_alone = True
        for direction in every_directions:
            tmp_pos = position + direction
            can_shoot_there = self.opponentGrid.areCoordsValid(tmp_pos)
            if can_shoot_there:
                cell = self.opponentGrid[tmp_pos]
                is_not_alone = (
                    cell == self.opponentGrid.SENT_TOUCHED_BOAT_CELL or
                    cell == self.opponentGrid.SENT_SANK_BOAT_CELL
                )
                if is_not_alone:
                    is_alone = False
                    break
        return is_alone

    def placeShips(self):
        playerInfo = self.playerInfo
        if playerInfo.readyToPlay:
            return

        half_grid = (self.model.GRID_SIZE-1)/2.
        for _ in range(6):
            randx = round(half_grid + 3*(0.5-random.random()))
            randy = round(half_grid + 3*(0.5-random.random()))
            self.playerGrid[randx, randy] = self.playerGrid.SHOULD_NOT_PUT_BOAT_CELL

        for boatSize in reversed(self.model.BOAT_SIZES):
            self.addBoat(self.__placeBoat(boatSize))
        self.__clearUnusedBoatCells()

        playerInfo.readyToPlay = True
        print('COMPUTER {} READY TO PLAY'.format(self.playerInfo.playerName))
        return

    def __placeBoat(self, boat_length):
        """
        WILL place a boat: is called recursively when it cannot.
        """
        grid_length = self.model.GRID_SIZE

        x = self.__randSig(grid_length)
        y = self.__randSig(grid_length)
        position = np.array([x, y])
        direction = self.__randSquareDir(x, y, grid_length)

        boat_cords = self.playerInfo.genBoatCoords(boat_length, position, direction)

        if not self.__canPlaceBoatHere(self.playerGrid, boat_cords):
            return self.__placeBoat(boat_length)

        for coord in boat_cords:
            self.playerGrid[tuple(coord)] = self.playerGrid.BOAT_CELL

            for _ in range(boat_length*2):
                r = self.__randDirAll()
                surrounding = coord + r
                if self.playerGrid.areCoordsValid(surrounding):
                    if self.playerGrid[tuple(surrounding)] == self.playerGrid.EMPTY_CELL:
                        self.playerGrid[tuple(surrounding)] = self.playerGrid.SHOULD_NOT_PUT_BOAT_CELL

        for coord in [boat_cords[0], boat_cords[-1]]:
            dirs = [direction, -direction]
            if boat_length > 3:
                dir1 = np.array(list(reversed(direction)))
                dirs.append(dir1)
                dirs.append(-dir1)
            for r in dirs:
                surrounding = coord + r
                if self.playerGrid.areCoordsValid(surrounding):
                    if self.playerGrid[tuple(surrounding)] == self.playerGrid.EMPTY_CELL:
                        self.playerGrid[tuple(surrounding)] = self.playerGrid.SHOULD_NOT_PUT_BOAT_CELL
        return boat_cords

    def __canPlaceBoatHere(self, grid, boat_cords, accept_shot_cells=False):
        """
        For the given boat coordinates, checks if a boat could be placed here.
        The boat can be placed if the cells at it's coordinates are all empty.
        """
        if not self.playerGrid.areCoordsValid(boat_cords):
            return False

        for coord in boat_cords:
            cell = grid[tuple(coord)]
            is_cell_unoccupied = cell == grid.EMPTY_CELL or (
                accept_shot_cells and cell == grid.SENT_TOUCHED_BOAT_CELL
            )

            if not is_cell_unoccupied:
                return False
        return True

    def __randDirAll(self):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        return np.array([x, y])

    def __randSquareDir(self, x, y, grid_length):
        """
        Get a direction randomly in the form of a tuple of (±1, 0) or (0, ±1).
        It can be altered to force a little more probability on a side rather
        than on the other depending of the position.
        """
        if random.randint(0, 2) != 0:
            halfGrid = grid_length/2
            x -= halfGrid
            y -= halfGrid
            ax = abs(x)
            ay = abs(y)
            sign = lambda num: (1, -1)[num<0]

            if ax > ay:
                direction = sign(x)*np.array([-1, 0])
            else:
                direction = sign(y)*np.array([0, -1])

            return direction

        is_x_dir = random.random()
        if is_x_dir > 0.5:
            x = int((random.randint(0, 1) - 0.5)*2)
            y = 0
        else:
            x = 0
            y = int((random.randint(0, 1) - 0.5)*2)
        return np.array([x, y])

    def __randSig(self, grid_length, forceSides=False):
        """
        Sigmoid function that has a better probability of placing boats on the map's corner two sides.
        """
        if forceSides and random.randint(0, 1) == 0:
            return random.randint(0, 1)*(grid_length-1)

        x = random.random() *(grid_length + 3) - 1.5
        grid_length = float(grid_length)
        boatIndex = int(grid_length/(1+math.exp(-(x/2-grid_length/4))))
        r = int(max(0, min(grid_length-1, boatIndex)))
        return r

    def __get2DSigGrid(self, grid_length, mean):
        """
        returns a 2D grid from rand_sig().
        """
        # Because the grid is an int grid for quick computations,
        # when rounded, the grid looses of its mean.
        magic_number = 1.5

        grid = np.zeros((grid_length, grid_length))
        for i in range(20*grid_length**2):
            grid[self.__randSig(grid_length), self.__randSig(grid_length)] += (
                1/20. * mean*magic_number
            )

        grid = grid.astype(int)

        return grid

    def __testRandSig(self, grid_length, mean):
        """
        To visualise the probability of rand_sig(10) a little bit.
        Function not used for production.
        """
        x = np.zeros(grid_length)

        for i in range(20*grid_length):
            x[self.__randSig(grid_length)] += 1/20. * mean
        import matplotlib.pyplot as plt
        plt.plot(range(grid_length), x)
        plt.plot(range(grid_length), np.zeros(grid_length))
        plt.show()

    def __clearUnusedBoatCells(self):
        """ Clear cells that were marked as to not host a boat after placing boats"""
        playerGrid = self.playerGrid
        pendingCells = playerGrid.getCellsWhere(
            playerGrid.SHOULD_NOT_PUT_BOAT_CELL)
        for cell in pendingCells:
            self.updateCell(playerGrid, cell, playerGrid.EMPTY_CELL)