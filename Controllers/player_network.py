#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Player class which is handling communication with the client_reseau
depending on the action of the game we're at. Acting as a gate between or
game architecture and the server.
"""
__auteur__ = "GUCHE29"
__date__ = "2015-12-05"
__coequipiers__ = "RAGAU72"

import time

from .client_reseau import ClientReseau, Protestation
from .player import Player
from Models import Model

class PlayerNetwork(Player):

    def __init__(self, playerInfo, view, p1_name):
        super().__init__(playerInfo, view)
        self.__client = ClientReseau(
            pseudo=p1_name, adversaire=playerInfo.playerName
        )
        self.playerInfo.playerName = self.__client.adversaire()
        self.remainingCells = sum(Model.BOAT_SIZES)

    def attack(self):
        target_cell = self.playerInfo.target_cell

        if target_cell is None:
            response = self.__client.attaquer(None)
            if response is not None:
                target_cell = (int(response[1]), int(response[4]))
            self.playerInfo.target_cell = target_cell

        return target_cell

    def placeShips(self):
        """
        The network player is always ready to play at the beginning of the game,
        because if not we will just wait longer when waiting for it's shot later.
        """
        self.playerInfo.readyToPlay = True

    def receiveShot(self, shotNPCoordinate):
        self.__client.attaquer(str(tuple(shotNPCoordinate)))

    def answer(self):
        response = self.__client.rapporter(None)
        if response == "à l'eau":
            return self.playerGrid.RECEIVED_SHOT_CELL
        elif response == "touché":
            self.__removeCell()
            return self.playerGrid.RECEIVED_TOUCHED_BOAT_CELL
        elif response == "coulé":
            self.__removeCell()
            return self.playerGrid.RECEIVED_SANK_BOAT_CELL
        elif response is None:
            time.sleep(1)
            print("Awaiting opponent's response...")
            return None
        else:
            print(response)
            self.__client.protester(
                "Je m'attendais à une réponse telle que \"à l'eau\", "
                "\"touché\" ou \"coulé\". A reçu: {}".format(response)
            )

    def __removeCell(self):
        self.remainingCells -= 1
        if self.remainingCells == 0:
            self.boats = []
            self.playerInfo.has_boats = False

    def addShot(self, shotNPCoordinate, opponentsResponse):
        """
        Do nothing, as the network opponent's is handling his own game.
        """
        message = "à l'eau"

        if opponentsResponse == self.opponentGrid.RECEIVED_TOUCHED_BOAT_CELL:
            message = "touché"

        if opponentsResponse == self.opponentGrid.RECEIVED_SANK_BOAT_CELL:
            message = "coulé"

        self.__client.rapporter(message=message)
        self.playerInfo.target_cell = None

    def beYelledAt(self, message):
        self.__client.protester(message)