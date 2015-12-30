#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Player factory which is building players depending on their
playerType id in the model. Instantiate the child player class
consequently.
"""
__author__ = "GUCHE29"
__date__ = "2015-12-05"
__teammates__ = "RAGAU72"

from .player_local_human import PlayerHuman
from .player_local_computer import PlayerComputer
from .player_network import PlayerNetwork

from Models.player_info import PlayerInfo


class PlayerFactory():
    @staticmethod
    def createPlayer(modelPlayerInfo, view, p1_name):
        """Create a player depending on their player id (static attribute
            from player_info."""

        if not isinstance(modelPlayerInfo, PlayerInfo):
            raise TypeError("modelPlayerInfo should be 'PlayerInfo' type.")

        if modelPlayerInfo.playerType == PlayerInfo.HUMAN:
            player = PlayerHuman(modelPlayerInfo, view)
        if modelPlayerInfo.playerType == PlayerInfo.COMPUTER:
            player = PlayerComputer(modelPlayerInfo, view)
        if modelPlayerInfo.playerType == PlayerInfo.NETWORK:
            player = PlayerNetwork(modelPlayerInfo, view, p1_name)

        return player