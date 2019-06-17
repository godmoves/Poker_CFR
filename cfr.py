# coding: utf-8
# This implements Counterfactual Regret Minimization in a general zero sum two
# player game.

import numpy as np

import best_response


def cfr(game, num_iters=10000):
    # regrets is a dictionary where the keys are the information sets and values
    # are dictionaries from actions available in that information set to the
    # counterfactual regret for not playing that action in that information set.
    # Since information sets encode the player, we only require one dictionary.
    regrets = dict()

    # Similarly, action_counts is a dictionary with keys the information sets
    # and values dictionaries from actions to action counts.
    action_counts = dict()

    # Strategy_t holds the strategy at time t; similarly strategy_t_1 holds the
    # strategy at time t + 1.
    strategy_t = dict()
    strategy_t_1 = dict()

    average_strategy = None
    average_strategy_snapshot = None

    # Each information set is uniquely identified with an action tuple.
    # values = {1: [], 2: []}
    for t in range(num_iters):
        for i in [1, 2]:
            cfr_recursive(game, game.game.root, i, t, 1.0, 1.0, regrets,
                          action_counts, strategy_t, strategy_t_1)

        if (t % 100 == 0) and (average_strategy is not None):
            print("t: {}".format(t))
            if average_strategy_snapshot is not None:
                snapshot_distance = compare_strategies(average_strategy, average_strategy_snapshot)
                print("Distance between strategies (t - 100): {:.10f}".format(snapshot_distance))

                # If the snapshot distance is small enough, then return the
                # average strategy.  This means that Euclidean distance between
                # the strategy at time t and at time t - 100 is small, which is
                # hopefully sufficient for convergence.
                if snapshot_distance < 1e-5:
                    complete_strategy = game.game.complete_strategy_uniformly(average_strategy)
                    exploitability = best_response.compute_exploitability(game.game, complete_strategy)
                    print("Avg strategy exploitability: {:.4f}".format(exploitability))
                    return average_strategy

            average_strategy_snapshot = average_strategy.copy()
        average_strategy = compute_average_strategy(action_counts)

        # Update strategy_t to equal strategy_t_1. We update strategy_t_1 inside
        # cfr_recursive.  We take a copy because we update it inside
        # cfr_recursive, and want to hold on to strategy_t_1 separately to
        # compare.
        strategy_t = strategy_t_1.copy()

        if t % 1000 == 0:
            # We also compute the best response to the current strategy.
            complete_strategy = game.game.complete_strategy_uniformly(strategy_t)
            exploitability = best_response.compute_exploitability(game.game, complete_strategy)
            print("Current strategy exploitability: {:.4f}".format(exploitability))

    complete_strategy = game.game.complete_strategy_uniformly(average_strategy)
    exploitability = best_response.compute_exploitability(game.game, complete_strategy)
    print("Avg strategy exploitability: {:.4f}".format(exploitability))
    return average_strategy


def compute_average_strategy(action_counts):
    average_strategy = dict()
    for information_set in action_counts:
        num_actions = sum([v for k, v in action_counts[information_set].items()])
        if num_actions > 0:
            average_strategy[information_set] = {
                k: float(v) / float(num_actions) for k, v in action_counts[information_set].items()}

    return average_strategy


def compare_strategies(s1, s2):
    """ Takes the average Euclidean distance between the probability distributions.
    """
    common_keys = [k for k in s1.keys() if k in s2.keys()]
    distances = []
    for information_set in common_keys:
        prob_dist_diff = [
            float(s1[information_set][a] - s2[information_set][a])**2 for a in s1[information_set]]
        distances.append(np.sqrt(np.mean(prob_dist_diff)))
    return np.mean(distances)


# The Game object holds a game state at any point in time, and can return an
# information set label for that game state, which uniquely identifies the
# information set and is the same for all states in that information set.
def cfr_recursive(game, node, i, t, pi_1, pi_2, regrets, action_counts,
                  strategy_t, strategy_t_1):
    # If the node is terminal, just return the payoffs
    if game.is_terminal(node):
        return game.payoffs(node)[i]
    # If the next player is chance, then sample the chance action
    elif game.which_player(node) == 0:
        a = game.sample_chance_action(node)
        return cfr_recursive(
            game, node.children[a], i, t, pi_1, pi_2,
            regrets, action_counts, strategy_t, strategy_t_1)

    # Get the information set
    information_set = game.information_set(node)

    # Get the player to play and initialise values
    player = game.which_player(node)
    value = 0
    available_actions = game.available_actions(node)
    values_Itoa = {a: 0 for a in available_actions}

    # Initialise strategy_t[information_set] uniformly at random.
    if information_set not in strategy_t:
        strategy_t[information_set] = {
            a: 1.0 / float(len(available_actions)) for a in available_actions}

    # Compute the counterfactual value of this information set by computing the counterfactual
    # value of the information sets where the player plays each available action and taking
    # the expected value (by weighting by the strategy).
    for a in available_actions:
        if player == 1:
            values_Itoa[a] = cfr_recursive(
                game, node.children[a], i, t, strategy_t[information_set][a] *
                pi_1, pi_2, regrets, action_counts, strategy_t, strategy_t_1)
        else:
            values_Itoa[a] = cfr_recursive(
                game, node.children[a], i, t, pi_1,
                strategy_t[information_set][a] * pi_2, regrets, action_counts,
                strategy_t, strategy_t_1)
        value += strategy_t[information_set][a] * values_Itoa[a]

    # Update regrets now that we have computed the counterfactual value of the
    # information set as well as the counterfactual values of playing each
    # action in the information set.  First initialise regrets with this
    # information set if necessary.
    if information_set not in regrets:
        regrets[information_set] = {ad: 0.0 for ad in available_actions}
    if player == i:
        for a in available_actions:
            pi_minus_i = pi_1 if i == 2 else pi_2
            pi_i = pi_1 if i == 1 else pi_2
            regrets[information_set][a] += (values_Itoa[a] - value) * pi_minus_i
            if information_set not in action_counts:
                action_counts[information_set] = {ad: 0.0 for ad in available_actions}
            action_counts[information_set][a] += pi_i * strategy_t[information_set][a]

        # Update strategy t plus 1
        strategy_t_1[information_set] = compute_regret_matching(regrets[information_set])

    # Return the value
    return value


def compute_regret_matching(regrets):
    """ Given regrets r_i for actions a_i, we compute the regret matching
    strategy as follows.  Define denominator = sum_i max(0, r_i). If denominator
    > 0, play action a_i proportionally to max(0, r_i).  Otherwise, play all
    actions uniformly.
    """

    # If no regrets are positive, just return the uniform probability
    # distribution on available actions.
    if max([v for k, v in regrets.items()]) <= 0.0:
        return {a: 1.0 / float(len(regrets)) for a in regrets}
    else:
        # Otherwise take the positive part of each regret (i.e. the maximum of
        # the regret and zero), and play actions with probability proportional
        # to positive regret.
        denominator = sum([max(0.0, v) for k, v in regrets.items()])
        return {k: max(0.0, v) / denominator for k, v in regrets.items()}


def evaluate_strategies(game, strategy, num_iters=500):
    """ Given a strategy in the form of a dictionary from information sets to
    probability distributions over actions, sample a number of games to
    approximate the expected value of player 1.
    """
    values = game.game.expected_value(strategy, strategy, num_iters)
    values_mean = np.mean(values)
    return values, values_mean
