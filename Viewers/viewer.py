#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" View initialization class.
"""
__author__ = "RAGAU72"
__date__ = "2015-12-05"
__teammates__ = "GUCHE29"

from .view_window import ViewWindow

class Viewer():
    def __init__(self, model):
        """Initialize the view of the program."""
        self.model = model
        self.view = ViewWindow(model)