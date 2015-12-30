
""" Script d'initialisation du programme qui va écouter les arguments
appelés pendant son exécution et générer le Modèle en conséquence.
Va ensuite générer le Viewer et le Controller.
"""
__auteur__ = "GUCHE29"
__date__ = "2015-12-05"
__coequipiers__ = "RAGAU72"

import argparse

from Models import Model
from Viewers import Viewer
from Controllers import Controller


def Main():
    parser = argparse.ArgumentParser(
        description='A battleship game built with Python. You can play versus the '
                    'computer or against someone else. Call the program with the '
                    'arguments described below to enable those features. The colors '
                    'of shots while playing represents the answer of the enemy. '
                    'Once the game has ended, the console will output the result.'
    )

    parser.add_argument('-n',
                        dest='network_player_name',
                        action='store', default=False,
                        help='Play against someone specific on the network "-n friendName", '
                             'versus someone random on the server "-n None", '
                             'or play against your computer without adding "-n". '
                             'If you play on the network and does not find someone to play '
                             'against within about 3 seconds, the game might freeze, '
                             'then just restart it to try again.')
    parser.add_argument('-c',
                        dest='is_local_player_comp',
                        action='store_true', default=False,
                        help='Add this argument to play as the computer against your opponent.')
    parser.add_argument('-s',
                        dest='is_display_disabled',
                        action='store_true', default=False,
                        help='Add this argument to disable display. Can only be set if '
                             'you play automatically as the computer. ')

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-u',
                               dest='username',
                               help='Set your username: "-u Your_Name".',
                               required=True)

    args = parser.parse_args()

    if args.is_display_disabled and not args.is_local_player_comp:
        # Do not raise as we do not want a stack trace.
        print('ERROR: Must play as computer to disable display. Add the "-c" argument.')
        return

    m = Model(args.username, not args.is_display_disabled, args.is_local_player_comp, args.network_player_name)
    v = Viewer(m)
    c = Controller(m, v.view)

if __name__ == "__main__":
    Main()
