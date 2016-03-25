# coding=utf-8
"""
Blackjack game which can by played by multiple users.  Currently,
the dealer will always stay on 17, regardless of whether the
hand is hard or soft (fairly common in most casinos).

© 2016 DAVID CALKINS ALL RIGHTS RESERVED
"""

import random

class Card(object):
    """
    Card object class.  Instantiates a card with name, suit, and value.
    """
    index_to_name = {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
                     8: "Eight", 9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King"}

    def __init__(self, index, suit):
        self.name = self.index_to_name[index]
        self.suit = suit
        self.value = min(index, 10)

    def display_card(self):
        """
        Return the name and suit of the card
        :return: (name, suit)
        """
        return self.name, self.suit

class Deck(object):
    """
    Class for building a shuffled 52-card deck and dealing cards.
    """
    def __init__(self):
        suits = ["Hearts", "Clubs", "Diamonds", "Spades"]
        self.deck = [
        Card(index, suit) for index in range(1, 14) for suit in suits]
        random.shuffle(self.deck)

    def deal_card(self):
        """
        Deal a card from the deck
        :return: Card object
        """
        return self.deck.pop()

class Hand(object):
    """
    Class for building a hand with cards from a deck instance.
    """
    def __init__(self, game_deck):
        self.hand = []
        self.game_deck = game_deck

    def deal_hand(self):
        """
        Return an initial hand consisting of two Card() objects in a list.
        :return: [Card1(), Card2()]
        """
        hand = self.hand[:]
        while len(hand) < 2:
            card = self.game_deck.deal_card()
            hand.append(card)

        return hand

    def display_cards(self, cards):
        """
        Return the name and suit of each card in the hand
        :param cards:
        :return: [(name1, suit1), (name2, suit2), (name3, suit3)...]
        """
        displayed = [card.display_card() for card in cards]

        return displayed

    def total_points(self, cards):
        """
        Return the total point value of the given hand.  If the player has
        a soft hand (two cards, one being an ace), a tuple of scores is
        returned, one where ace = 1, and one where ace = 11.
        :param cards:
        :return: int or tuple
        """

        values = [card.value for card in cards]
        total = sum(values)
        # Returns high and low scores if hand is a soft hand
        for card in cards:
            if card.name == 'Ace' and total + 10 < 21:
                low_total = total
                high_total = total + 10

                return low_total, high_total

        else:
            return total

    def is_blackjack(self, cards):
        """
        Returns True if there are two cards in the hand, one being an Ace
        and the other having a value of 10.
        :param cards:
        :return: bool
        """
        names = [card.name for card in cards]
        values = [card.value for card in cards]

        if len(cards) == 2:
            if 'Ace' in names and 10 in values:
                return True
            else:
                return False

class DealerHand(Hand):
    """
    Subclass of Hand() for building the dealers's hand.  Contains
    rules for the dealers total as well as automatic hit rules.

    """

    def display_visible_cards(self, cards):
        """
        Display only the dealer's visible card
        :param cards:
        :return: list (should only have one card in it)
        """
        return self.display_cards(cards)[1:]

    def total_points(self, cards):
        """
        Overrides method of Hand() class.  Dealer only needs the higher score
        returned if the hand is soft.
        :return: int
        """
        values = [card.value for card in cards]
        total = sum(values)

        for card in cards:
            if card.name == 'Ace' and total + 10 < 21:
                total += 10

        return total

    def dealer_should_hit(self, total):
        """
        Returns True if score < 17
        :param: cards
        :return: bool
        """
        if total < 17:
            return True
        else:
            return False

        ## Below are rules where the dealer must hit on a soft 17.  Might add
        # an option for this setting later.
        # if type(total) == tuple and total[1] <= 17:
        #     return True
        #
        # # For a hard hand, the dealer hits if the score is < 17.
        # elif type(total) == int and total < 17:
        #     return True
        #
        # else:
        #     return False

def main():
    pass

if __name__ == '__main__':
    main()



