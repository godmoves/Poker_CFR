# coding: utf-8

import numpy as np


class CFRGame():
    """ A CFRGame implements a few extra functions to make CFR work.
    """

    def __init__(self, game):
        self.game = game

    def payoffs(self, node):
        """ If the action sequence is terminal, returns the payoffs for players
        1 and 2 in a dictionary with keys 1 and 2.
        """
        return node.utility

    def is_terminal(self, node):
        """ Returns True/False if the action sequence is terminal or not.
        """
        return node.player == -1

    def which_player(self, node):
        """ Returns the player who is to play following the action sequence.
        """
        return node.player

    def available_actions(self, node):
        """ Returns the actions available to the player to play.
        """
        return [a for a in node.children.keys()]

    def sample_chance_action(self, node):
        """ If the player for the game state corresponding to the action
        sequence is the chance player, then sample one of the available actions.
        Return the action.
        """
        assert node.player == 0
        actions = [a for a in node.chance_probs]
        probs = [v for a, v in node.chance_probs.items()]
        return np.random.choice(actions, p=probs)

    def information_set(self, node):
        """ Returns a unique hashable identifier for the information set
        containing the action sequence. This could be a tuple with the
        actions that are visible to the player. The information set belongs
        to the player who is to play following the action sequence.
        """
        return self.game.info_set_ids[node]
