#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Abstract class which is hadling two types of player : human and AI.
"""
__author__ = "RAGAU72"
__date__ = "2015-12-05"
__teammates__ = "GUCHE29"

import abc

from .player import Player
from .client_reseau import Protestation

class PlayerLocal(Player):
    @abc.abstractmethod
    def __init__(self, playerInfo, view):
        super().__init__(playerInfo, view)

    @abc.abstractmethod
    def attack(self):
        """Attack abstract method, defined in child class."""
        pass

    def updateCell(self, grid, cell, state):
        """Update the state of a cell in the grid and will
        draw it in the view if the player is P1 the view is only
        available for p1."""
        grid[cell] = state
        if self.playerInfo.isP1:
            self.view.iconsToDraw.append(cell + (state,))

    @abc.abstractmethod
    def placeShips(self): pass

    def receiveShot(self, shotNPCoordinate):
        """Receive a shot from the opponent by some coordinates.
        Update the state of the player defense grid.
        """
        # Answer is not done yet, how and when should we implement it in the game ?

        receiving_attack_cell_status = self.playerGrid[shotNPCoordinate]
        if receiving_attack_cell_status == self.playerGrid.BOAT_CELL:
            receiving_attack_cell_status = self.playerGrid.RECEIVED_TOUCHED_BOAT_CELL
            self.updateCell(self.playerGrid, shotNPCoordinate, self.playerGrid.RECEIVED_TOUCHED_BOAT_CELL)
            is_boat_sank = self.playerInfo.removeBoatHitFromEnnemyWhere(shotNPCoordinate)
            if is_boat_sank:
                receiving_attack_cell_status = self.playerGrid.RECEIVED_SANK_BOAT_CELL
        elif receiving_attack_cell_status == self.playerGrid.EMPTY_CELL:
            receiving_attack_cell_status = self.playerGrid.RECEIVED_SHOT_CELL
            self.updateCell(self.playerGrid, shotNPCoordinate, self.playerGrid.RECEIVED_SHOT_CELL)
        self.response = receiving_attack_cell_status

    def answer(self):
        """return the attacked cell in receiveShot depending on what was there."""
        return self.response

    def addBoat(self, boatNPCoordinates):
        """Add a boat from a certain set of rows and columns
        row and column must be arrays in this architecture []"""
        boat = []
        for coord in boatNPCoordinates:
            self.updateCell(self.playerGrid, tuple(coord), self.playerGrid.BOAT_CELL)
            boat.append(tuple(coord))
        self.playerInfo.boats.append(boat)

    def addShot(self, shotNPCoordinate, opponentsResponse):
        """Add a shot in the attack grid depending on the opponent's response."""
        attacked_cell_status = self.opponentGrid.SENT_SHOT_CELL

        if opponentsResponse == self.opponentGrid.RECEIVED_TOUCHED_BOAT_CELL:
            attacked_cell_status = self.opponentGrid.SENT_TOUCHED_BOAT_CELL

        if opponentsResponse == self.opponentGrid.RECEIVED_SANK_BOAT_CELL:
            attacked_cell_status = self.opponentGrid.SENT_SANK_BOAT_CELL
            self.playerInfo.updateEstimatedRemainingEnnemyBoats(shotNPCoordinate)

        self.updateCell(self.opponentGrid, shotNPCoordinate, attacked_cell_status)

        # Reset the cell target.
        self.playerInfo.target_cell = None

    def getCheatingStatus(self, p2):
        """
        Call the methods for network cheating if needed.
        """
        if False:
            p2.beYelledAt("From {}: You cheated.".format(self.playerInfo.playerName))
        return

    def beYelledAt(self, message):
        raise Protestation(message)