# coding: utf-8
# This implements One Card Poker.

from deepstack.extensive_game import ExtensiveGame, ExtensiveGameNode


class OneCardPoker(ExtensiveGame):
    """ This is the game described on 'http://www.cs.cmu.edu/~ggordon/poker/'.
    Rules: each player is privately dealt one card from a deck of 'n_cards'
    cards (without replacement). Currently there is one card for each card
    value. Each player antes 1 chip (a forced initial bet). Player 1 then bets
    either 0 or 1. Player 2 can fold (if player 1 bet 1), match player 1's bet,
    or, if player 1 bet 0, then player 2 can raise by betting 1. In the last
    situation, player 1 then gets a chance to match the bet or fold.
    """

    @staticmethod
    def compute_utility(betting_actions, hole_cards):
        """ Given actions in 'betting_actions' and hole_cards in 'hole_cards',
        compute the utility for both players at a terminal node.
        """
        # The bets are 1 (for the ante), then the sum of the even actions (for
        # player 1) and the odd actions (for player 2).
        bets = {1: 1.0, 2: 1.0}
        for i, action in enumerate(betting_actions):
            bets[(i % 2) + 1] += action
        winner = 1 if hole_cards[1] > hole_cards[2] else 2
        loser = 2 if hole_cards[1] > hole_cards[2] else 1
        # The winner wins the amount the loser bet, and the loser loses this
        # amount.
        return {winner: bets[loser], loser: -bets[loser]}

    @staticmethod
    def create_one_card_tree(action_list, cards):
        """ Creates a tree for one card Poker. 'cards' is a list of numbers of
        cards, defining the deck. The numbers should be unique. Initially this
        should be called with 'action_list' being an empty list.
        """
        if len(action_list) == 0:
            # We are at the root of the tree, so we create a chance node for
            # player 1.
            root = ExtensiveGameNode(0)
            # This node is hidden from player 2
            root.hidden_from = [2]
            for card in cards:
                # Create a game tree below this node.
                root.children[card] = OneCardPoker.create_one_card_tree(
                    [card], cards)
                root.chance_probs[card] = 1.0 / len(cards)
            return ExtensiveGame(root)
        elif len(action_list) == 1:
            # We are at a chance node for player 2, so we create this chance
            # node, including its children.
            node = ExtensiveGameNode(0)
            # This node is hidden from player 1
            node.hidden_from = [1]
            for card in cards:
                # Player 2 can't be dealt the card that player 1 was dealt.
                if card == action_list[0]:
                    continue
                # Otherwise create a child node below
                node.children[card] = OneCardPoker.create_one_card_tree(
                    action_list + [card], cards)
                node.chance_probs[card] = 1.0 / (len(cards) - 1.0)
            return node
        elif len(action_list) == 2:
            # It's player 1's first turn.
            node = ExtensiveGameNode(1)
            node.children[0] = OneCardPoker.create_one_card_tree(
                action_list + [0], cards)
            node.children[1] = OneCardPoker.create_one_card_tree(
                action_list + [1], cards)
            return node
        elif len(action_list) == 3:
            # It's player 2's first turn.
            node = ExtensiveGameNode(2)
            node.children[0] = OneCardPoker.create_one_card_tree(
                action_list + [0], cards)
            node.children[1] = OneCardPoker.create_one_card_tree(
                action_list + [1], cards)
            return node
        elif len(action_list) == 4:
            # It's player 1's second turn (if the node isn't terminal).
            if action_list[3] == 0 or action_list[2] == action_list[3]:
                # The second player folded, or called a bet of 0, or called a
                # bet of 1. Thus this node is terminal.
                node = ExtensiveGameNode(-1)
                hole_cards = {1: action_list[0], 2: action_list[1]}
                node.utility = OneCardPoker.compute_utility(
                    action_list[2:], hole_cards)
                return node
            else:
                # The actions were [0,1], and so player 1 gets another chance to
                # call or fold.
                node = ExtensiveGameNode(1)
                node.children[0] = OneCardPoker.create_one_card_tree(
                    action_list + [0], cards)
                node.children[1] = OneCardPoker.create_one_card_tree(
                    action_list + [1], cards)
                return node
        elif len(action_list) == 5:
            # It's player 2's second turn (but this actually must be terminal).
            node = ExtensiveGameNode(-1)
            hole_cards = {1: action_list[0], 2: action_list[1]}
            node.utility = OneCardPoker.compute_utility(
                action_list[2:], hole_cards)
            return node
        assert False

    @staticmethod
    def create_game(n_cards):
        """ Creates the One Card Poker game, with the given number of uniquely
        numbered cards in the deck, numbered 1 up to n_cards.
        """
        game_tree = OneCardPoker.create_one_card_tree([], range(1, n_cards + 1))
        return game_tree
