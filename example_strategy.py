# coding: utf-8
import numpy as np


def random_distribution(n_items):
    """ Returns a random probability distribution over n items. Formally, we
    choose a point uniformly at random from the n-1 simplex.
    """
    return np.random.dirichlet([1.0 for i in range(n_items)])


def uniformly_random_strategy(game, player):
    """ Returns a dictionary from information set identifiers to probabilities
    over actions for the given player. The distribution is always uniform over
    actions.
    - game is an ExtensiveGame instance.
    """
    info_sets = game.info_set_ids

    # Restrict to information sets where the given player has to take an action.
    player_info_sets = {k: v for k, v in info_sets.items() if k.player == player}

    # Now randomly generate player 1's strategy and player 2's strategy. Define
    # a strategy as being a dictionary from information set identifiers to
    # probabilities over actions available in that information set.
    strategy = {}
    for node, identifier in player_info_sets.items():
        actions = node.children.keys()
        # Only need to add to the strategy for nodes whose information set has
        # not been included already.
        if identifier not in strategy:
            # Sample actions uniformly at random. Can change this later.
            strategy[identifier] = {a: 1.0 / float(len(actions)) for a in actions}

    return strategy


def dirichlet_random_strategy(game, player):
    """ We return a dictionary from information set identifiers to probabilities
    over actions for the given player.
    - game is an ExtensiveGame instance.
    """
    info_sets = game.build_information_sets(player)

    # Restrict to information sets where the given player has to take an action.
    player_info_sets = {k: v for k, v in info_sets.items() if k.player == player}

    # Now randomly generate player 1's strategy and player 2's strategy. Define
    # a strategy as being a dictionary from information set identifiers to
    # probabilities over actions available in that information set.
    strategy = {}
    for node, identifier in player_info_sets.items():
        actions = node.children.keys()
        # Only need to add to the strategy for nodes whose information set has
        # not been included already.
        if identifier not in strategy:
            # Sample actions uniformly at random. Can change this later.
            probs = random_distribution(len(actions))
            strategy[identifier] = {a: p for a, p in zip(actions, probs)}

    return strategy


def constant_action_strategy(game, player, action):
    """ This strategy always plays action 'action'. We return a dictionary from
    information set identifiers to probabilities over actions for the given
    player.
    - game is an ExtensiveGame instance.
    """
    info_sets = game.build_information_sets(player)

    # Restrict to information sets where the given player has to take an action.
    player_info_sets = {k: v for k, v in info_sets.items() if k.player == player}

    # Now randomly generate player 1's strategy and player 2's strategy. Define
    # a strategy as being a dictionary from information set identifiers to
    # probabilities over actions available in that information set.
    strategy = {}
    for node, identifier in player_info_sets.items():
        actions = node.children.keys()
        # Only need to add to the strategy for nodes whose information set has
        # not been included already.
        if identifier not in strategy:
            # Play the action specified. If it's not available, play uniformly
            # over all actions.
            strategy[identifier] = {a: 0.0 for a in actions}
            if action in actions:
                strategy[identifier][action] = 1.0
            else:
                strategy[identifier] = {a: 1.0 / len(actions) for a in actions}

    return strategy
