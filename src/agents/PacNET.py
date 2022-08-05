"""
========================================================

        Introduction to artificial intelligence

                         PacNET

========================================================
@ Victor Mangeleer - S181670

-------------
Documentation
-------------

This file contains the AI behind our PacNET

"""
import os
import sys
 
from others.data import *
from module.game import Agent
from collections import Counter
from others.data import generateData

# Adding missing folder
sys.path.insert(0, str(os.path.abspath('')).replace("src", "model/others"))

from training import *
from data_model import *


#----------------------------------------------------------
#
#                     Parameters of PacNET
# 
#----------------------------------------------------------
# Define the version of PacNET that should be used
pacnet_version = "PacNET"


#----------------------------------------------------------
#
#                         PacNET Agent
# 
#----------------------------------------------------------
class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """

        # This list will contains all the moves Pacman will execute
        self.moves = []

        # Loading the model
        self.model = loadModel("../model/PacNETs/", pacnet_version)

    def get_action(self, state, generate_Data):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - Given a pacman game state, returns a legal move
          which is defined in `game.Directions`.
        """

        # 1 - If Pacman has no move available, we try to find some
        # by using the A star algorithm on the current game state.
        if not self.moves:
            self.moves = self.PacNET(state)

        # 2 - We try to return an action.
        try:
            return self.moves.pop(0)

        # 3 - No actions are available so we trigger an exception.
        except IndexError:
            return Directions.STOP

    def PacNET(self, state):

        # Transformation of the current game state into an input
        (x, _) = generateData(state, "_")

        # Conversion to readable format
        x = np.asarray(x)
        x = torch.from_numpy(np.flip(x, axis=0).copy())
        x = x.unsqueeze(0)

        # Computing SBOT prediction
        pred = self.model(x.float())

        # Adding the move
        return getMove(pred)
