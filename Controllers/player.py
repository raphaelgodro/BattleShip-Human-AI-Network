#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Abstract class for ai, human and network players.
"""
__author__ = "GUCHE29"
__date__ = "2015-12-05"
__teammates__ = "RAGAU72"

import abc

class Player():
    def __init__(self, playerInfo, view):
        """Initialization of the abstract player class.
        Organise the attributes common to each players type."""
        self.playerInfo = playerInfo
        self.view = view
        self.model = view.model
        self.playerGrid = playerInfo.getGrid(playerInfo.PLAYER_GRID)
        self.opponentGrid = playerInfo.getGrid(playerInfo.OPPONENT_GRID)

    @abc.abstractmethod
    def attack(self):
        pass

    @abc.abstractmethod
    def placeShips(self): pass

    @abc.abstractmethod
    def receiveShot(self, shotNPCoordinate): pass

    @abc.abstractmethod
    def answer(self): pass

    @abc.abstractmethod
    def placeShips(self): pass

    @abc.abstractmethod
    def updateCell(self, grid, cell, state): pass

    @abc.abstractmethod
    def addShot(self, shotNPCoordinate, opponentsResponse): pass

    @abc.abstractmethod
    def beYelledAt(self, message): pass
