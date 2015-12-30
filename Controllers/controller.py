#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Controller main class. Defines the structure of the game and
call the player controllers method.
"""
__author__ = "RAGAU72"
__date__ = "2015-12-05"
__teammates__ = "GUCHE29"

import time

from .player_factory import PlayerFactory
from .client_reseau import Protestation

class Controller():
    def __init__(self, model, view):
        """Controller initialisation method which separates
        the game in two main steps : initGame for boat placing
        and playGame for the game loop."""
        self.m = model
        self.v = view

        self.p1 = PlayerFactory.createPlayer(model.player1, view, model.player1.playerName)
        self.p2 = PlayerFactory.createPlayer(model.player2, view, model.player1.playerName)

        self.__initGame()
        self.__playGame()

    def __initGame(self):
        """Wait until every player are done with
        the boat placement."""
        model = self.m
        p1 = self.p1
        p2 = self.p2

        while not model.players_ready_to_play:
            self.v.screen.listen()
            p1.placeShips()
            p2.placeShips()
            self.v.refresh()
            if p1.playerInfo.readyToPlay and p2.playerInfo.readyToPlay:
                model.players_ready_to_play = True
        print("")

    def __playGame(self):
        """Play the game and exchange information of player plays
        during the turn. Makes games turn until someone has no remaining
        boats. """
        model = self.m
        p1 = self.p1
        p2 = self.p2

        number_of_exchanged_shots = 0

        try:
            while not model.is_game_finished:
                self.v.screen.listen()

                p1_shot = None
                while p1_shot is None:
                    p1_shot = p1.attack()
                    self.v.refresh()

                p2.receiveShot(p1_shot)

                p2_shot = None
                while p2_shot is None:
                    p2_shot = p2.attack()
                    self.v.refresh()

                p1.receiveShot(p2_shot)

                p1_response = None
                while p1_response is None:
                    p1_response = p1.answer()
                    self.v.refresh()
                p2.addShot(p2_shot, p1_response)
                self.v.refresh()

                p2_response = None
                while p2_response is None:
                    p2_response = p2.answer()
                    self.v.refresh()
                p1.addShot(p1_shot, p2_response)
                self.v.refresh()

                # handle error for network player: declare cheat or win
                p1.getCheatingStatus(p2)  # This method can raise a Protestation() exception.
                # Don't do this: p2.getCheatingStatus()
                # As it is not implemented for PlayerNetwork nor abstract in the Player class.

                time.sleep(0.01)
                number_of_exchanged_shots += 1

                if not p1.playerInfo.has_boats or not p2.playerInfo.has_boats:
                    model.is_game_finished = True
        except Protestation as p:
            print("A player protested. Message : {}".format(p))

        self.v.refresh()
        print('GAME DONE:')
        print("P1 remaining boat count: {}".format(len(p1.playerInfo.boats)))
        print("P2 remaining boat count: {}".format(len(p2.playerInfo.boats)))
        print("Number of exchanged shots: {}".format(number_of_exchanged_shots))

        time.sleep(2.5)
        # TODO: Show that game has ended in UI and manage to
        # replace the time.sleep of auto-closing with an exit button.
