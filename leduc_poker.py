# coding: utf-8
# This implements Leduc Hold'em.

from extensive_game import ExtensiveGame, ExtensiveGameNode


class LeducPoker(ExtensiveGame):
    """
    """
    @staticmethod
    def compute_bets(action_list):
        """ Given a list of actions, compute the current bets by players 1 and
        2. The action_list should include the hole cards for the players.
        """
        # Both players ante 1
        bets = {1: 1, 2: 1}
        other_player = {1: 2, 2: 1}

        if len(action_list) <= 2:
            return bets
        # Remove the hole cards.
        action_list = action_list[2:]

        # Player 1 starts round 1 and player 2 starts round 2.
        player = 1

        # The raise amount is 2 in the first round and 4 in the second round.
        raise_amount = 2
        for action in action_list:

            if action >= 10:
                # This was a card, so ignore it but increment the round counter.
                raise_amount = 4
                player = 2
            if action == 0:
                # Fold
                return bets
            elif action == 1:
                # Check/call
                # Update the bet of the current player to equal the bet of the
                # other player
                bets[player] = bets[other_player[player]]
            elif action == 2:
                # Bet/Raise
                # First call the bet of the other player, and then add the
                # betting amount to
                # player's bet.
                bets[player] = bets[other_player[player]]
                bets[player] += raise_amount
            # Switch players
            player = other_player[player]
        return bets

    @staticmethod
    def compute_utility(action_list):
        """ Given actions in 'action_list', including the cards dealt, compute
        the utility for both players at a terminal node.
        """
        bets = Leduc.compute_bets(action_list)
        hole_cards = {1: action_list[0], 2: action_list[1]}
        board = [a for a in action_list[2:] if a >= 10][0]

        if hole_cards[1] == board:
            winner = 1
        elif hole_cards[2] == board:
            winner = 2
        elif hole_cards[1] > hole_cards[2]:
            winner = 1
        else:
            winner = 2
        loser = 1 if winner == 2 else 2
        # The winner wins the amount the loser bet, and the loser loses this
        # amount.
        return {winner: bets[loser], loser: -bets[loser]}

    @staticmethod
    def create_leduc_tree(action_list, cards):
        """ Creates a tree for Leduc Hold'em. 'cards' is a list of numbers of
        cards, defining the remainder of the deck from this node onwards (i.e.
        excluding cards that have been dealt). Initially this should be called
        with 'action_list' being an empty list.
        """
        if len(action_list) == 0:
            # We are at the root of the tree, so we create a chance node for
            # player 1.
            root = ExtensiveGameNode(0)
            # This node is hidden from player 2
            root.hidden_from = [2]
            for card in cards:
                # Create a game tree below this node.
                if card not in root.children:
                    remaining_cards = cards.copy()
                    remaining_cards.remove(card)
                    root.children[card] = Leduc.create_leduc_tree(
                        action_list + [card], remaining_cards)
                    root.chance_probs[card] = 1.0 / float(len(cards))
                else:
                    root.chance_probs[card] += 1.0 / float(len(cards))
            return ExtensiveGame(root)
        elif len(action_list) == 1:
            # We are at a chance node for player 2, so we create this chance
            # node, including its children.
            node = ExtensiveGameNode(0)
            # This node is hidden from player 1
            node.hidden_from = [1]
            for card in cards:
                # Otherwise create a child node below
                if card not in node.children:
                    remaining_cards = cards.copy()
                    remaining_cards.remove(card)
                    node.children[card] = Leduc.create_leduc_tree(
                        action_list + [card], remaining_cards)
                    node.chance_probs[card] = 1.0 / float(len(cards))
                else:
                    node.chance_probs[card] += 1.0 / float(len(cards))
            return node

        # We have dealt both players a card. We first see which round we are in.
        betting_rounds = []
        betting_round = []
        board_cards = []
        for a in action_list[2:]:
            # If a < 10, then a is an action.
            if a < 10:
                betting_round.append(a)
            else:
                # Otherwise a denotes a card.
                board_cards.append(a)
                if len(betting_round) > 0:
                    betting_rounds.append(betting_round)
                    betting_round = []
        if len(betting_round) > 0:
            betting_rounds.append(betting_round)

        # We have now split up the actions into betting rounds and cards.
        # Should now have a list of betting rounds in 'betting_rounds', with the
        # second one potentially being incomplete. We also potentially have
        # board cards in 'board_cards'.

        # If there is only one betting round in rounds, then we are still in
        # the first round. Otherwise we are in the second.

        # Check if it's the end of the round.
        assert len(betting_rounds) <= 2

        if len(betting_rounds) == 0:
            betting_round = []
        else:
            betting_round = betting_rounds[-1]

        if betting_round == [1, 1] or betting_round[-2:] == [2, 1] or \
           betting_round[-2:] == [2, 0]:
            # The round is terminal. The next node should be a chance
            # node, but we may have already created it. We can check
            # this by the number of cards on the board.

            # If we are in round 1, then we create the chance node.
            if len(betting_rounds) == 1:
                if len(board_cards) > 0:
                    # We have already created the chance node, so now we are
                    # in a player 2 node (player 2 goes first in round 2).
                    # They have the actions check and raise available.
                    node = ExtensiveGameNode(2)
                    node.children[1] = Leduc.create_leduc_tree(
                        action_list + [1], cards)
                    node.children[2] = Leduc.create_leduc_tree(
                        action_list + [2], cards)
                    return node
                else:
                    # We need to create the chance node for the board.
                    node = ExtensiveGameNode(0)
                    for card in cards:
                        if card not in node.children:
                            remaining_cards = cards.copy()
                            remaining_cards.remove(card)
                            node.children[card] = Leduc.create_leduc_tree(
                                action_list + [card], remaining_cards)
                            node.chance_probs[card] = 1.0 / float(len(cards))
                        else:
                            node.chance_probs[card] += 1.0 / float(len(cards))
                    return node
            else:
                # This is the end of the game. So compute utilities.
                node = ExtensiveGameNode(-1)
                node.utility = Leduc.compute_utility(action_list)
                return node
        else:
            # The round is not terminal. We first find out whose turn it
            # is: even number of actions means player 1, else player 2.
            player = 1 if len(betting_round) % 2 == 0 else 2
            node = ExtensiveGameNode(player)
            # The available actions are:
            if betting_round == []:
                available_actions = [1, 2]
            elif betting_round == [2]:
                available_actions = [0, 1, 2]
            elif betting_round == [2, 2]:
                available_actions = [0, 1, 2]
            elif betting_round == [2, 2, 2]:
                available_actions = [0, 1, 2]
            elif betting_round == [2, 2, 2, 2]:
                available_actions = [0, 1]
            elif betting_round == [1]:
                available_actions = [1, 2]
            elif betting_round == [1, 2]:
                available_actions = [0, 1, 2]
            elif betting_round == [1, 2]:
                available_actions = [0, 1, 2]
            elif betting_round == [1, 2, 2]:
                available_actions = [0, 1, 2]
            elif betting_round == [1, 2, 2, 2]:
                available_actions = [0, 1, 2]
            elif betting_round == [1, 2, 2, 2, 2]:
                available_actions = [0, 1]

            # Now create the child node for each available action:
            for action in available_actions:
                node.children[action] = Leduc.create_leduc_tree(
                    action_list + [action], cards)
            return node

    @staticmethod
    def create_game(n_cards):
        """ Creates the Leduc Poker game, with the given number of numbered
        cards in the deck, numbered 9 + 1 up to 9 + n_cards, each repeated
        twice.
        """
        game_tree = Leduc.create_leduc_tree(
            [], 2 * [a for a in range(10, n_cards + 10)])
        return game_tree
