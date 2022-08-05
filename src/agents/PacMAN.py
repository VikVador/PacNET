"""
========================================================

        Introduction to artificial intelligence

                         PacNET

========================================================
@ Victor Mangeleer - S181670

-------------
Documentation
-------------

This file contains the AI behind our best playing Pacman. It is used
to either show how it plays or to generate data for PacNET

"""

import numpy as np

from module.game import Agent
from collections import Counter
from others.data import generateData
from module.pacman import Directions
from others.maze import maze_retrieve

# Global variables
maze_map      = {}
food_dots     = []
closed_states = []


def key(state):
    """
    Creates a key that uniquely identifies a Pacman game state.

    Arguments:
    ----------
    - 'state': the current game state. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """

    return (state.getFood(), state.getPacmanPosition(),
            state.getGhostPosition(1), state.getGhostDirection(1))


def player(depth):
    """
    Determines which player's turn it is.

    Arguments:
    ----------
    - 'depth' : the depth of the current state.

    Returns:
    --------
    0 or 1 whether it's Pacman or the ghost's turn.
    """

    # Pacman's turn, it corresponds to an even depth.
    if (depth % 2) == 0:
        return 0

    # Ghost's turn, it corresponds to an odd depth.
    else:
        return 1


def cutoff_test(state, depth):
    """
    Indicates if the search in the tree of
    possibilities must stop or not.

    Arguments :
    -----------
    - 'state' : the current game state.

    - 'depth' : the level of the node containing 'state' in the tree.

    Return :
    --------
    - True or False whether the condition to stop
      the recursion has been reached in 'state'.
    """

    # 1 - Initialization of variables
    p_pos = state.getGhostPosition(1)

    g_pos = state.getPacmanPosition()

    # 2 - Conditions of recursion,
    # A) Over the status of the state
    if state.isWin() is True or state.isLose() is True:
        return True

    # B) Over the status of the cell : if the
    # cell contains a food dot and the ghost is far
    # enough not to eat Pacman, it stops

    # Retrieves the distance between Pacman and the ghost
    ghost_dist = maze_retrieve(state, p_pos, g_pos, maze_map)

    if p_pos in food_dots and ghost_dist > 4:
        return True

    # C) Over the quiescence : if the ghost is far
    # from Pacman, it's less likely to have big changes
    elif ghost_dist > (6 - depth) and ghost_dist > 2:
        return True

    # D) Over a depth treshold
    elif depth == 8:
        return True

    # E) Keep searching
    else:
        return False


def evals(state, depth):
    """
    Evaluates the value of a game state.

    Arguments :
    -----------

    - 'state' : the current game state.

    - 'depth' : the level of the node containing 'state' in the tree.

    Returns :
    ---------
    - The value corresponging to the given state
    """

    # 1 - Initialization of variables
    p_pos = state.getPacmanPosition()
    g_pos = state.getGhostPosition(1)

    # 3 - Stores the different distances calculated.
    distances_food = []

    # 4 - Computation of the perfect distance for the food dots
    i = 0

    while i < len(food_dots):

        # Retrieves position of a dot
        food_pos = food_dots[i]

        # Compute the distance
        distances_food.append(maze_retrieve(state, p_pos, food_pos, maze_map))

        i = i + 1

    # 5 - Ghost's distance from Pacman
    distance_ghost = maze_retrieve(state, p_pos, g_pos, maze_map)

    # 6 - Computation of the returned value
    return (distance_ghost + state.getScore() - 3 * min(distances_food))


def hminimax_rec(node, closed):
    """
    It is used by the h-minimax function in order to
    find the optimal next move (recursiv part of the algorithm)

    Arguments:
    ----------
    - 'node': turple containing a state and its depth in the
              tree of possibilities

    - 'closed': list of all the states already explored

    Return:
    -------
    - The utility score of a given state and the updated list
      of states already explored
    """

    # Newclosed contains all the visited states on the direct
    # path to the given state.
    newclosed = closed.copy()

    # Adds the state's key to the list of state already explored
    newclosed.append(key(node[0]))

    # 1 - Verifies if the state is an ending state
    if cutoff_test(node[0], node[1]) is True:

        # Return the utility value of the state and
        # the updated list of state already visited
        return evals(node[0], node[1])

    # 2 - The current state is not an ending state, the
    # algorithm goes deeper in the tree
    else:

        # Contains the values used to find the next best move
        values = []

        # Pacman's turn
        if player(node[1]) == 0:

            # Looks for the next best move in the successors
            for next_state, action in node[0].generatePacmanSuccessors():

                ns_key = key(next_state)

                # Only look at states not explored
                if ns_key not in newclosed and ns_key not in closed_states:

                    # Determine the utility value of the next state
                    evaluation = hminimax_rec(
                        [next_state, node[1] + 1], newclosed)

                    # Adds the utility value to the list
                    values.append(evaluation)

            # Checks if there are values available to be returned
            # i.e. at least one child state not already visited
            if len(values) > 0:
                return max(values)
            else:
                return 5000

        # Ghost's turn
        elif player(node[1]) == 1:

            # Looks for the next best move in the successors
            for next_state, action in node[0].generateGhostSuccessors(1):

                ns_key = key(next_state)

                # Only look at states not explored
                if ns_key not in newclosed and ns_key not in closed_states:

                    # Determine the utility value of the next state
                    evaluation = hminimax_rec(
                        [next_state, node[1] + 1], newclosed)

                    # Adds the utility value to the list
                    values.append(evaluation)

            # Checks if there are values available to be returned
            if len(values) > 0:
                return min(values)
            else:
                return -5000


class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """

        # This list will contains all the moves Pacman will execute
        self.moves = []

    def get_action(self, state, generate_Data):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - 'state': the current game state. See FAQ and class
                   `pacman.GameState`.

        - 'generate_Data' : Choose to generate or not data based 
                            on the game played

        Return:
        -------
        - Given a pacman game state, returns a legal move
          which is defined in `game.Directions`.
        """

        # 1 - If Pacman has no move available, we try to find some
        # by using the A star algorithm on the current game state.
        if not self.moves:
            self.moves = self.hminimax(state)

        # 2 - We try to return an action.
        try:
            
            # Retreives the current move
            move = self.moves.pop(0)

            #-----------------------
            # Generation of the data
            #-----------------------
            if generate_Data == 1:

                # Input data
                (x, y) = generateData(state, move)

                # Opening files
                x_file = open('../data/x.txt','a')
                y_file = open('../data/y.txt','a')

                # Saving the results
                x_file.write("<\n")
                y_file.write("<\n")
                np.savetxt(x_file, x, fmt='%f')
                np.savetxt(y_file, y, fmt='%f')

                # Closing files
                x_file.close()
                y_file.close()

                # Determination of a random movement
                nb_move = np.random.randint(5, size = 1)

                # List of the possible movements
                movements = ["North", "South", "East", "West"]

                # Force teaching
                ft = np.random.randint(2, size=1)

                if ft == 1:
                    return move #movements[nb_move[0]]
                else:
                    return move
            else:
                return move


        # 3 - No actions are available so we trigger an exception.
        except IndexError:
            return Directions.STOP

    def hminimax(self, state):
        """
        Given a pacman game state, returns the optimal
        next move for pacman

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A move as defined in `game.Directions`.
        """

        # 1 - Initialization of variables

        # Contains the values used to find
        # the next best move
        value = []

        # Contain the legal actions associatedto
        # each values whose corresponding state has
        # not been yet visited and the corresponding states
        action_list = []
        state_list = []

        # Contain all legal actions and the corresponding states
        # Used when all children states has already been visited
        action_list_bis = []
        state_list_bis = []

        # Contains a list of the state already explored for each successor
        closed = []

        # Contains the number of occurence of the successor
        # of the current state in closed_states
        occurence = []

        # Contains all the states Pacman went through
        # between each call of h-minimax
        global closed_states

        # It is a list of the position of every dots in the game,
        # in order to not go through the food matrix each time
        # we want to look for them
        global food_dots

        # Initialization of the list if it's the first time
        if len(food_dots) == 0:

            # Retrieves the size of the maze
            food_position = state.getFood()

            length = 0
            for boolean in food_position:
                length = length + 1

            width = len(food_position[0])

            # Retrieves the position of the dots
            i = j = 0

            while i < length:

                while j < width:

                    if food_position[i][j] is True:
                        food_dots.append((i, j))

                    j = j + 1

                i = i + 1
                j = 0

        # 2 If Pacman eats a dot, we have to remove it from the list
        p_pos = state.getPacmanPosition()

        if p_pos in food_dots:

            # Remove the dots that has been eaten
            food_dots.pop(food_dots.index(p_pos))

        # Add the current state to the two list of visited ones
        # because it is played in the actual game and also belongs
        # to all the direct paths to a given state.
        closed.append(key(state))
        closed_states.append(key(state))

        # 3 - Looks for the next best move
        for next_state, action in state.generatePacmanSuccessors():

            ns_key = key(next_state)

            action_list_bis.append(action)

            state_list_bis.append(next_state)

            # Only look at states not explored
            if ns_key not in closed and ns_key not in closed_states:

                # Contains a state and its depth in the tree
                node = [next_state, 1]

                # Determine the utility value of the next state
                evaluation = hminimax_rec(node, closed)

                # Adds the utility value of the next state into the list
                value.append(evaluation)

                # Adds the action related to the next state
                action_list.append(action)
                state_list.append(next_state)

        # When a move is not legal, we set is evaluation
        # value to +-5000. We have to remove these values
        # in order to find the best move (5000 is a convention)
        a = len(value) - 1

        while a >= 0:

            # |5000| is our convention for an illegal move
            if abs(value[a]) == 5000:

                # Remove the possibility
                value.pop(a)
                action_list.pop(a)
                state_list.pop(a)

            a = a - 1

        # 4 - Returns the best action
        if len(value) != 0:

            index_best_action = value.index(max(value))

            closed_states.append(key(state_list[index_best_action]))

            return [action_list[index_best_action]]

        # 5 - All children have already been visited, we look for
        # an action in the less visited state
        elif len(value) == 0:

            # Count how many times each state in closed_states has been visited
            all_occurence = Counter(closed_states)

            # As all states has been visited at least once, the least visited
            # state is chosen as next state.
            b = 0
            for action_bis in action_list_bis:

                # Counts how many times the given state
                # appears in closed_states
                occurence.append(all_occurence[key(state_list_bis[b])])
                b = b + 1

            # Removes losing state from the list
            c = 0
            for action_bis in action_list_bis:

                if state_list_bis[c].isLose() is True:

                    occurence.pop(c)

                    state_list_bis.pop(c)

                    action_list_bis.pop(c)

                c = c + 1

            # Retrieves the action related to the least visited state
            index_min = occurence.index(min(occurence))

            closed_states.append(key(state_list_bis[index_min]))

            return [action_list_bis[index_min]]
