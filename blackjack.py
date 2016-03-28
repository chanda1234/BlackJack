# coding=utf-8
"""
Blackjack game which can by played by multiple users.  Currently,
the dealer will always stay on 17, regardless of whether the
hand is hard or soft (fairly common in most casinos).

© 2016 DAVID CALKINS ALL RIGHTS RESERVED
"""

import random
import sys

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

    def full_name(self):
        """
        Return full name of the card (e.g., 'King of Diamonds'}
        :param: card
        :return: string
        """
        return '{0} of {1}'.format(self.display_card()[0], self.display_card()[1])

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
        for card in cards:

            if card.name == 'Ace':
                if total + 10 < 21:
                    low_total = total
                    high_total = total + 10
                    return low_total, high_total

                if total + 10 == 21:
                    total += 10

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
            if card.name == 'Ace' and total + 10 <= 21:
                total += 10

        return total

    def dealer_should_hit(self, total):
        """
        Returns True if score < 17
        :param: cards
        :return: bool
        """

        if type(total) == int:
            if total < 17:
                return True
            else:
                return False
        else:
            raise TypeError("Expected type(total) to be int, got type{0}".format(total))

    def dealer_should_stay(self, total):
        if type(total) == int:
            if 17 <= total <= 21:
                return True
            else:
                return False
        else:
            raise TypeError("Expected type(total) to be int, got type{0}".format(total))

def deal_all_hands(number_of_players, deck):
    """
    Populate a list of all players' hands
    :param: num_players (int), deck
    """
    hands = []
    for num in range(1, number_of_players+1):
        player_hand = Hand(deck)
        hands.append(player_hand.deal_hand())

    return hands

def get_current_players_cards(player_number, player_hands):
    """
    Return the hand from the list of player_hands which
    corresponds to the player number.
    :param: player_number, player_hands (list of Hand objects)
    :return: Hand(obj)
    """
    for tup in enumerate(player_hands, 1):
        if tup[0] == player_number:
            current_players_hand = tup[1]
            return current_players_hand

def add_new_card_to_hand(cards, deck):
    """
    Return new hand with updated card list [(card1, name1), (card2, name2)...]
    :param: current_hand (list of tuples as shown above), deck
    :return: updated list of cards in hand
    """
    new_card = deck.deal_card()
    new_hand = cards[:]
    new_hand.append(new_card)

    return new_hand


def main():
    deck = Deck()
    player_scores = {}
    print "\n"
    print "#####################################"
    print "###########   BLACKJACK  ############"
    print "#####################################"
    print "\n"

    while True:
        user_input = raw_input("Enter number of players (maximum seven): ")
        try:
            number_of_players = int(user_input)
            if not 0 < number_of_players < 8:
                print "Number of players must be between 1 and 7\n"
            else:
                break
        except ValueError:
            print "Please enter a number.\n"

    dealer_hand = DealerHand(deck)
    dealer_cards = dealer_hand.deal_hand()
    first_face_up_card = dealer_hand.display_visible_cards(dealer_cards)[0]

    for player_num in range(1, number_of_players + 1):
        hand = Hand(deck)
        cards = hand.deal_hand()
        displayed_cards = hand.display_cards(cards)
        print "------------PLAYER {0} TURN------------\n".format(player_num)
        print "DEALER SHOWING: {0} of {1}\n".format(first_face_up_card[0], first_face_up_card[1])
        print "CURRENT HAND: "
        print "------------"

        for card in displayed_cards:
            print "{0} of {1}".format(card[0], card[1])
        print "\n"

        if hand.is_blackjack(cards):
            print "** PLAYER {0} BLACKJACK! **".format(player_num)
            player_scores[player_num] = 'blackjack'
            continue
        else:
            print "CURRENT SCORE: {0}".format(hand.total_points(cards))

        score = hand.total_points(cards)

        while True:
            hit_or_stay = raw_input("Hit? (y/n): ")
            no_responses = ['N', 'n', 'No', 'no']
            yes_responses = ['Y', 'y', 'Yes', 'yes']
            print "\n"
            if hit_or_stay not in yes_responses and hit_or_stay not in no_responses:
                print "Please enter either Yes or No"

            if hit_or_stay in yes_responses:
                cards = add_new_card_to_hand(cards, deck)
                player_hit_msg = "** PLAYER {0} HITS **\n".format(player_num)
                player_21_msg = "** PLAYER {0} SCORES 21! **".format(player_num)
                player_bust_msg = "** PLAYER {0} BUSTS! **\n".format(player_num)
                current_hand_msg = "CURRENT HAND: ".format(player_num)
                print player_hit_msg
                print current_hand_msg
                print "------------"
                for card in cards:
                    print "{0} of {1}".format(card.display_card()[0], card.display_card()[1])
                print "\n"

                score = hand.total_points(cards)
                print "CURRENT SCORE: {0}".format(score)

                if type(score) == int:
                    if score > 21:
                        print player_bust_msg
                        if number_of_players > 1:
                            break
                        else:
                            sys.exit()
                    elif score == 21:
                        print player_21_msg
                        player_scores[player_num] = score
                        break
                    else:
                        pass

                # If the score is a tuple, there is a soft ace in the hand.
                if type(score) == tuple:
                    pass

            if hit_or_stay in no_responses:
                player_stays_msg = "** PLAYER {0} STAYS WITH {1} **\n".format(player_num, score)
                if type(score) == tuple:
                    score = score[1]
                player_scores[player_num] = score
                print player_stays_msg
                break

    dealer_score = dealer_hand.total_points(dealer_cards)
    print "------------DEALER'S TURN------------\n"
    print "CURRENT HAND: "
    print "------------"
    for card in dealer_cards:
        print card.full_name()
    print "CURRENT SCORE: {0}\n".format(dealer_score)

    # Check for blackjack first
    if dealer_hand.is_blackjack(dealer_cards):
        print "** DEALER BLACKJACK **"
        print "** DEALER WINS **"
        sys.exit()

    # If the dealer should not hit, (score > 17) dealer stays,
    # and the 'hit' loop below will be skipped.
    if not dealer_hand.dealer_should_hit(dealer_score):
        print "** DEALER STAYS WITH {0} **".format(dealer_score)

    else:
        while dealer_score < 17:
            if dealer_hand.dealer_should_hit(dealer_score):
                print "** DEALER HITS **\n"
                dealer_cards = add_new_card_to_hand(dealer_cards, deck)
                dealer_score = dealer_hand.total_points(dealer_cards)

                for card in dealer_cards:
                    print card.full_name()
                print "CURRENT SCORE: {0}\n".format(dealer_score)

        # Check if the dealer should stay, or if the dealer busted
        if dealer_hand.dealer_should_stay(dealer_score):
            print "** DEALER STAYS WITH {0} **\n".format(dealer_score)

        elif dealer_score > 21:
            print "** DEALER BUSTS **"

if __name__ == '__main__':
    main()



