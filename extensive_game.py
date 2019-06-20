# coding: utf-8

import numpy as np


class ExtensiveGameNode:
    """ A class for a game node in an extensive form game.
    """

    def __init__(self, player):
        # Which player is to play in the node. Use -1 for terminal, 0 for
        # chance, 1 for player 1, 2 for player 2.
        self.player = player

        # A dictionary of children for the node. Keys are the actions in the
        # node, and values are ExtensiveGameNode objects resulting from taking
        # the action in this node.
        self.children = {}

        # Who can see the actions in this node.
        self.hidden_from = []

        # Utility of the node to each player (as a dictionary). Only relevant
        # for terminal nodes.
        self.utility = {}

        # If the node is a chance node, then store the chance probs. This is a
        # dictionary with keys the actions and probs the probability of choosing
        # this action.
        self.chance_probs = {}


class ExtensiveGame:

    def __init__(self, root):
        # set the root node.
        self.root = root

        # Also build the information set ids.
        self.info_set_ids = self.build_info_set_ids()

    @staticmethod
    def print_tree_recursive(node, action_list, only_leaves):
        """ Prints out a list of all nodes in the tree rooted at 'node'.
        """
        if only_leaves and len(node.children) == 0:
            print(action_list, node.utility)
        elif not only_leaves:
            print(action_list)
        for action, child in node.children.items():
            ExtensiveGame.print_tree_recursive(
                child, action_list + [action], only_leaves)

    def print_tree(self, only_leaves=False):
        """ Prints out a list of all nodes in the tree by the list of actions
        needed to get to each node from the root.
        """
        ExtensiveGame.print_tree_recursive(self.root, [], only_leaves)

    def build_information_sets(self, player):
        """ Returns a dictionary from nodes to a unique identifier for the
        information set containing the node. This is all for the given player.
        """
        info_set = {}

        # We just recursively walk over the tree using a stack to store the
        # nodes to explore.
        node_stack = [self.root]
        visible_actions_stack = [[]]

        # First build the information sets for player 1.
        while len(node_stack) > 0:
            node = node_stack.pop()
            visible_actions = visible_actions_stack.pop()

            # Add the information set for the node, indexed by the
            # visible_actions list, to the information set dictionary. Use a
            # tuple instead of a list so that it is hashable if we want later
            # on.
            info_set[node] = tuple(visible_actions)

            for action, child in node.children.items():
                # Add all the children to the node stack and also the visible
                # actions to the action stack. If an action is hidden from the
                # player, then add -1 to signify this.
                node_stack.append(child)
                if player in node.hidden_from:
                    visible_actions_stack.append(visible_actions + [-1])
                else:
                    visible_actions_stack.append(visible_actions + [action])

        return info_set

    def build_info_set_ids(self):
        """ Join the two info set dictionaries. The keys are nodes in the game
        tree belonging to player 1 or player 2, and the values are the
        identifier for the information set the node belongs to, from the
        perspective of the player to play in the node.
        """
        info_sets_1 = self.build_information_sets(1)
        info_sets_2 = self.build_information_sets(2)
        info_set_ids = {}
        for k, v in info_sets_1.items():
            if k.player == 1:
                info_set_ids[k] = v
        for k, v in info_sets_2.items():
            if k.player == 2:
                info_set_ids[k] = v
        return info_set_ids

    def expected_value(self, strategy_1, strategy_2, num_iters):
        """ Given a strategy for player 1 and a strategy for player 2, compute
        the expected value for player 1.
        - strategy_1: should be a dictionary from information set identifiers
          for player 1 for all of player 1's nodes to probabilities over actions
          available in that information set.
        - strategy_2: same for player 2.
        Returns the result of each game of strategy_1 versus strategy_2.
        """
        results = []
        for t in range(num_iters):
            node = self.root
            while node.player != -1:
                # Default to playing randomly.
                actions = [a for a in node.children.keys()]
                probs = [1.0 / float(len(actions)) for a in actions]

                # If it's a chance node, then sample an outcome.
                if node.player == 0:
                    probs = node.chance_probs.values()
                elif node.player == 1:
                    # It's player 1's node, so use their strategy to make a
                    # decision.
                    info_set = self.info_set_ids[node]
                    if info_set in strategy_1:
                        probs = strategy_1[info_set].values()
                elif node.player == 2:
                    # It's player 2's node, so use their strategy to make a
                    # decision.
                    info_set = self.info_set_ids[node]
                    if info_set in strategy_2:
                        probs = strategy_2[info_set].values()

                probs = [p for p in probs]

                # Make sure the probabilities sum to 1
                assert abs(1.0 - sum(probs)) < 1e-5

                # Sample an action from the probability distribution.
                action = np.random.choice(np.array(actions), p=np.array(probs))

                # Move into the child node.
                node = node.children[action]

            # The node is terminal. Add the utility for player 1 to the results.
            results.append(node.utility[1])

        return results

    def complete_strategy_uniformly(self, strategy, verbose=True):
        """ Given a partial strategy, i.e. a dictionary from a subset of the
        info_set_ids to probabilities over actions in those information sets,
        complete the dictionary by assigning uniform probability distributions
        to the missing information sets.
        """
        new_strategy = strategy.copy()
        num_missing = 0
        for node, info_set_id in self.info_set_ids.items():
            if info_set_id not in new_strategy:
                actions = node.children.keys()
                new_strategy[info_set_id] = {
                    a: 1.0 / float(len(actions)) for a in actions}
                num_missing += 1
        if num_missing > 0 and verbose:
            print("Completed strategy at {} information sets.".format(num_missing))
        return new_strategy
