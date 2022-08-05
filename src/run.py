"""
========================================================

        Introduction to artificial intelligence

                         PacNET

========================================================
@ Victor Mangeleer - S181670

"""

from others.display import *
from argparse import ArgumentParser, ArgumentTypeError
from module.pacman import runGame, load_agent_from_file
from module.ghostAgents import GreedyGhost, SmartyGhost, DumbyGhost, EastRandyGhost

# Definition of the different ghosts that will be used during game
ghosts = {}
ghosts["greedy"]     = GreedyGhost
ghosts["smarty"]     = SmartyGhost
ghosts["dumby"]      = DumbyGhost
ghosts["rightrandy"] = EastRandyGhost

if __name__ == '__main__':

    # Defining game parameters
    parser = ArgumentParser()
    parser.add_argument(
        '--seed',
        help='Seed for random number generator',
        type=int,
        default=-1)
    parser.add_argument(
        '--agentfile',
        help='Python file containing a `PacmanAgent` class.',
        default="PacHUMAN.py")
    parser.add_argument(
        '--ghostagent',
        help='Ghost agent available in the `ghostAgents` module.',
        choices=["dumby", "greedy", "smarty", "rightrandy"], default="greedy")
    parser.add_argument(
        '--layout',
        help='Maze layout (from layout folder).',
        default="map_1.lay")
    parser.add_argument(
        '--nghosts',
        help='Maximum number of ghosts in a maze.',
        type=int, default=4)
    parser.add_argument(
        '--hiddenghosts',
        help='Whether the ghost is graphically hidden or not.',
        default=False, action="store_true")
    parser.add_argument(
        '--silentdisplay',
        help="Disable the graphical display of the game.",
        action="store_true")
    parser.add_argument(
        '--bsagentfile',
        help='Python file containing a `BeliefStateAgent` class.',
        default=None)
    parser.add_argument(
        '--w',
        help='Parameter w as specified in instructions for Project Part 3.',
        type=int, default=1)
    parser.add_argument(
        '--p',
        help='Parameter p as specified in instructions for Project Part 3.',
        type=float, default=0.25)
    parser.add_argument(
        '--generate',
        help='Choose to generate or not data based on the game played',
        type=int, default=0)
    args = parser.parse_args()

    # Terminal UI
    if args.generate == 0:
        PacNET_Logo()

    # Loading the Pacman agent
    agent = load_agent_from_file("agents/" + args.agentfile, "PacmanAgent")(args)

    # Loading the ghosts
    gagt = ghosts[args.ghostagent]
    nghosts = args.nghosts
    if (nghosts > 0):
        gagts = [gagt(i + 1, args) for i in range(nghosts)]
    else:
        gagts = []

    # Loading the game map
    layout = "module/layouts/" + args.layout

    # Terminal UI
    if args.generate == 0:
        PacNET_Game(args.agentfile)

    # Runnning the game
    total_score, total_computation_time, total_expanded_nodes = runGame(layout, agent, gagts, 
                                                                        None, not args.silentdisplay, args.generate,
                                                                        expout=0, hiddenGhosts=args.hiddenghosts)




