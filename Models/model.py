#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Model Initialisation class
"""
__author__ = "GUCHE29"
__date__ = "2015-12-05"
__teammates__ = "RAGAU72"

from .player_info import PlayerInfo

class Model():
    GRID_SIZE = 10
    BOAT_SIZES = [5, 4, 3, 3, 2]

    def __init__(self, username, is_display_enabled, is_local_player_comp, network_player_name):
        self.turn = 0
        self.players_ready_to_play = False
        self.is_game_finished = False
        self.is_display_enabled = is_display_enabled

        self.__setP1(username, is_local_player_comp)
        self.__setP2(network_player_name)

    def __setP1(self, username, is_computer):
        """ Defines which player is P1"""
        if is_computer:
            p1Type = PlayerInfo.COMPUTER
        else:
            p1Type = PlayerInfo.HUMAN
        self.player1 = PlayerInfo(username, p1Type, isP1=True)

    def __setP2(self, network_name):
        """Define which player is P2 """
        if isinstance(network_name, str) or isinstance(network_name, type(None)):
            p2Type = PlayerInfo.NETWORK
        elif isinstance(network_name, type(False)):
            p2Type = PlayerInfo.COMPUTER
        self.player2 = PlayerInfo(network_name, p2Type, isP1=False)