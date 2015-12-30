#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" View_window class that works with turtle.
Contain a cell stack drawn each time the refresh method
is called.
"""
__author__ = "RAGAU72"
__date__ = "2015-12-05"
__teammates__ = "GUCHE29"

import turtle


class ViewWindow():
    CELL_WIDTH = 40

    GRID_MARGINTOP = 100
    GRID_MARGINLEFT = 60
    GRID_MARGINRIGHT = 60
    GRID_MARGINBOTTOM = 100
    GAP_BETWEEN_GRIDS = 100

    BACKGROUND_COLOR = "#ffeebb"
    FILL_COLOR = "#335555"

    EMPTY_CELL_COLOR = 0
    BOAT_CELL_COLOR = "#ffeebb"
    SHOT_CELL_COLOR = "#07b8f2"
    TOUCHED_BOAT_CELL_COLOR = "#ff5500"
    SANK_BOAT_CELL_COLOR = "#ff0000"
    PENDING_BOAT_CELL_COLOR = "#ffffff"


    def __init__(self, model):
        """Initialize the view at the starting of the application."""
        self.model = model

        self.cellWidth = self.CELL_WIDTH
        self.model = model
        self.gridSize = model.GRID_SIZE
        self.player = self.model.player1
        self.screen = turtle.Screen()
        self.gridWidth = self.CELL_WIDTH * self.gridSize
        self.playerGrid = self.player.getGrid(self.player.PLAYER_GRID)
        self.enemyGrid = self.player.getGrid(self.player.OPPONENT_GRID)
        self.iconsToDraw = []

        turtle.title('BATTLESHIP : {} vs {}'.format(
            self.model.player1.playerName, self.model.player2.playerName))
        self.__setScreen()
        self.__setColor()
        turtle.tracer(0, 0)

        gridWidth = self.gridWidth
        gridAnchorPoints = []
        gridAnchorPoints.append((
            -self.width/2 + self.GRID_MARGINLEFT,
            self.height/2 - self.GRID_MARGINTOP - gridWidth))
        gridAnchorPoints.append((
            self.width/2 - gridWidth - self.GRID_MARGINRIGHT,
            self.height/2 - self.GRID_MARGINTOP - gridWidth ))

        self.__drawGrid(gridAnchorPoints[0], gridWidth)
        self.__drawGrid(gridAnchorPoints[1], gridWidth)

        self.gridAnchorPoints = gridAnchorPoints

    def __setScreen(self):
        """set the screen/window depending on view static attributes."""
        turtle.resizemode('noresize')
        self.width = self.GRID_MARGINLEFT + 2 * self.gridWidth + self.GAP_BETWEEN_GRIDS + self.GRID_MARGINRIGHT
        self.height = self.GRID_MARGINTOP + self.gridWidth + self.GRID_MARGINBOTTOM
        turtle.setup(width=self.width + 10, height=self.height + 10)
        turtle.screensize(self.width, self.height)
        turtle.bgpic("Ressources/fire_ocean.gif")
        turtle.reset()

    def __setColor(self):
        """Set background color and starting fill color."""
        turtle.bgcolor(self.BACKGROUND_COLOR)
        turtle.fillcolor(self.FILL_COLOR)

    def __drawSquare(self, x1, y1, x2, y2):
        """Draw a point from two diagonals of the square."""
        self.__drawLine(x1, y1, x2, y1)
        self.__drawLine(x2, y1, x2, y2)
        self.__drawLine(x2, y2, x1, y2)
        self.__drawLine(x1, y2, x1, y1)

    def __drawGrid(self, anchorPoint, gridWidth):
        """draw grid from bottom left anchor point"""
        x1 = anchorPoint[0] + gridWidth
        y1 = anchorPoint[1] + gridWidth
        x2 = anchorPoint[0]
        y2 = anchorPoint[1]
        turtle.begin_fill()
        self.__drawSquare(x1, y1, x2, y2)
        turtle.end_fill()

        cellWidth = self.CELL_WIDTH
        # draw horizontal lines
        for i in range(self.gridSize):
            self.__drawLine(x1,
                y2 + i*cellWidth,
                x2,
                y2 + i*cellWidth)
        # draw vertical lines
        for i in range(self.gridSize):
            self.__drawLine(x2 + i*cellWidth,
                y1,
                x2 + i*cellWidth,
                y2)

    def __drawLine (self, x1, y1, x2, y2):
        """Draw a line from a point to another."""
        turtle.penup()
        turtle.goto(x1, y1)
        turtle.pendown()
        turtle.goto(x2, y2)
        turtle.penup()

    def getCell(self, x, y, gridID):
        """Get X,Y cell from screen x,y """
        gridWidth = self.gridWidth
        anchorPointGrid = self.gridAnchorPoints[gridID]
        anchorPtX = anchorPointGrid[0]
        anchorPtY = anchorPointGrid[1]

        if x >= anchorPtX and x <= anchorPtX + gridWidth and y >= anchorPtY and y <= anchorPtY + gridWidth :
            cellX = int((x - anchorPtX) / self.CELL_WIDTH)
            cellY = int((y - anchorPtY) / self.CELL_WIDTH)
            return (cellX, cellY)
        else:
            return None

    def getXYFromCell(self, cell, gridID):
        """Get Screen X,Y from cell x,y """
        x, y = cell
        cellWidth = self.cellWidth
        anchorPointGrid = self.gridAnchorPoints[gridID]
        anchorPtX = anchorPointGrid[0]
        anchorPtY = anchorPointGrid[1]
        return (anchorPtX + x*cellWidth , anchorPtY + y*cellWidth)

    def refresh(self):
        """Refresh the grid."""
        self.iconFactory()
        turtle.update()

    def iconFactory(self):
        """Draw the symbols from the new play executed
            at a given cell.
        """
        playerGrid = self.playerGrid
        for icon in self.iconsToDraw:

            x, y, iconID = icon

            if iconID == playerGrid.EMPTY_CELL:
                self.drawCell((x, y), self.player.PLAYER_GRID, self.FILL_COLOR)

            elif iconID == playerGrid.BOAT_CELL:
                self.drawCell((x, y), self.player.PLAYER_GRID, self.BOAT_CELL_COLOR)

            elif iconID == playerGrid.RECEIVED_SHOT_CELL:
                self.drawCell((x, y), self.player.PLAYER_GRID, self.SHOT_CELL_COLOR)
            elif iconID == playerGrid.SENT_SHOT_CELL:
                self.drawCell((x, y), self.player.OPPONENT_GRID, self.SHOT_CELL_COLOR)

            elif iconID == playerGrid.RECEIVED_TOUCHED_BOAT_CELL:
                self.drawCell((x, y), self.player.PLAYER_GRID, self.TOUCHED_BOAT_CELL_COLOR)
            elif iconID == playerGrid.SENT_TOUCHED_BOAT_CELL:
                self.drawCell((x, y), self.player.OPPONENT_GRID, self.TOUCHED_BOAT_CELL_COLOR)

            elif iconID == playerGrid.RECEIVED_SANK_BOAT_CELL:
                self.drawCell((x, y), self.player.PLAYER_GRID, self.SANK_BOAT_CELL_COLOR)
            elif iconID == playerGrid.SENT_SANK_BOAT_CELL:
                self.drawCell((x, y), self.player.OPPONENT_GRID, self.SANK_BOAT_CELL_COLOR)


            # SENT_SANK_BOAT_CELL = 7
            # RECEIVED_SANK_BOAT_CELL = 8

            elif iconID == playerGrid.PENDING_BOAT_CELL:
                self.drawCell((x, y), self.player.PLAYER_GRID, self.PENDING_BOAT_CELL_COLOR)
        self.iconsToDraw = []

    def drawCell(self, cell, gridID, color):
        """Draw a certain cell with a certain color on a certain grid"""
        x1, y1 = self.getXYFromCell(cell, gridID)
        x2 = x1 + self.cellWidth
        y2 = y1 + self.cellWidth

        turtle.fillcolor(color)
        turtle.begin_fill()
        self.__drawSquare(x1, y1, x2, y2)
        turtle.end_fill()

