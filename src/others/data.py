"""
========================================================

        Introduction to artificial intelligence

                         PacNET

========================================================
@ Victor Mangeleer - S181670

-------------
Documentation
-------------

This file contains functions used to extract data from 
the Pacman game. They will be used to train our PacNET

"""

import numpy as np


# Takes into consideration the walls such that
# it gives an additionnal information about the possible moves
def getPositionValue(x, y, walls):

    value = 0

    # Adding value if wall is detected
    for i in [-1, 1]:
        for j in [-1, 1]:
            if walls[x + i][y + j] == True:
                value += 1

    return value


# This function generates the data of a game instance at time t.
def generateData(state, move):

    # Information about the game state
    foods = state.getFood()
    walls = state.getWalls()
    g_pos = state.getGhostPosition(1)
    p_pos = state.getPacmanPosition()

    # Dimensions of the map
    length = 0
    for boolean in foods:
        length = length + 1
    width = len(foods[0])

    #---------
    # x - data
    #---------
    x = np.ndarray(shape=(length, width), dtype=int)

    for i in range(length):
        for j in range(width):

            # Walls
            if walls[i][j] == True:
                x[i][j] = 1

            # Food dot
            elif foods[i][j] == True:
                x[i][j] = 2

            # Ghost
            elif g_pos == (i, j):
                x[i][j] = 3 + getPositionValue(i, j, walls)

            # Pacman
            elif p_pos == (i, j):
                x[i][j] = 8 + getPositionValue(i, j, walls)

            # Empty cell
            else:
                x[i][j] = 12

    # Normalization of the cells
    x = x/12

    # Editing the vector to shape it like the actual maze
    x = x.transpose()
    x = np.flip(x, 0)

    #---------
    # y - data
    #---------
    y = np.zeros(4)

    if move == "North":
        y[0] = 1
    if move == "South":
        y[1] = 1
    if move == "East":
        y[2] = 1
    if move == "West":
        y[3] = 1

    return (x, y)
