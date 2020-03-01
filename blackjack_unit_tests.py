"""
Unit tests for blackjack.py.
"""

import unittest
import mock
import blackjack

class testDeckClasses(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.Deck()
        self.hand = blackjack.Hand(self.deck)
        self.card = blackjack.Card(12, 'Any suit')

    def test_create_deck_card_hand(self):
        self.assertIsInstance(self.deck, blackjack.Deck)
        self.assertIsInstance(self.hand, blackjack.Hand)
        self.assertIsInstance(self.card, blackjack.Card)

class testCardClass(unittest.TestCase):

    def setUp(self):
        self.card = (blackjack.Card(12, 'Any suit'))

    def test_return_card_features(self):
        self.assertEqual(self.card.name, "Queen")
        self.assertEqual(self.card.suit, "Any suit")
        self.assertEqual(self.card.value, 10)

class testDeckClass(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.Deck()

    def test_get_52_card_deck(self):
        self.assertEqual(len(self.deck.deck), 51)
    # Expected Output: 52, should FAIL

    @mock.patch('blackjack.random')
    def test_call_shuffle_on_deck(self, mock_random):
        self.assertFalse(mock_random.shuffle.called)
        blackjack.Deck()
        self.assertTrue(mock_random.shuffle.called)

    def test_check_deal_card_returns_card(self):
        card = self.deck.deal_card()
        self.assertIsInstance(card, blackjack.Card)
        self.assertEqual(len(self.deck.deck), 51)

    def test_check_deal_card_modifies_count(self):
        card = self.deck.deal_card()
        card2 = self.deck.deal_card()
        self.assertIsInstance(card, blackjack.Card)
        self.assertIsInstance(card2, blackjack.Card)
        self.assertEqual(len(self.deck.deck), 51)
        # Expected Output: 50, should FAIL

class testHandClass(unittest.TestCase):

    def setUp(self):
        self.hand = blackjack.Hand(blackjack.Deck())
        self.dealer_hand = blackjack.DealerHand(blackjack.Deck())
        self.example_hard_cards = [blackjack.Card(
            13, 'Diamonds'), blackjack.Card(4, 'Clubs')]
        self.example_soft_cards = [blackjack.Card(1, 'Hearts'),
                                   blackjack.Card(6, 'Diamonds')]
        self.example_blackjack_cards = [blackjack.Card(1, 'Spades'),
                                        blackjack.Card(13, 'Hearts')]

    def test_display_cards(self):
        displayed = self.hand.display_cards(self.example_hard_cards)
        self.assertEqual([('King', 'Diamonds'), ('Four', 'Clubs')],
                         displayed)

    def test_display_dealers_visible_card(self):
        visible_cards = self.dealer_hand.display_visible_cards(
            self.example_hard_cards)
        self.assertEqual(visible_cards, [('Four', 'Clubs')])

    def test_total_points_is_sum(self):
        vals_from_hard_hand = [card.value for card in self.example_hard_cards]
        self.assertEqual(self.hand.total_points(self.example_hard_cards),
                         14)
        self.assertEqual(self.hand.total_points(self.example_hard_cards), sum(
            vals_from_hard_hand))

    def test_soft_hand_total_returns_tuple(self):
        self.assertEqual(self.hand.total_points(
            self.example_soft_cards), (7, 17))

    def test_hand_is_blackjack(self):
        self.assertTrue(self.hand.is_blackjack(self.example_blackjack_cards))
        self.assertFalse(self.hand.is_blackjack(self.example_hard_cards))
        self.assertEqual(self.hand.total_points(self.example_blackjack_cards), 21)
        self.assertEqual(self.dealer_hand.total_points(self.example_blackjack_cards), 21)

    def test_dealer_should_hit(self):
        # Lowest possible score on a hand is two points.
        for total in range(2, 22):
            if total < 17:
                self.assertTrue(self.dealer_hand.dealer_should_hit(total))
            else:
                self.assertFalse(self.dealer_hand.dealer_should_hit(total))

    def test_dealer_should_stay(self):
        for total in range(2, 22):
            if 17 <= total <= 21:
                self.assertTrue(self.dealer_hand.dealer_should_stay(total))
            else:
                self.assertFalse(self.dealer_hand.dealer_should_stay(total))

class TestMain(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.Deck()
        self.dealer_hand = blackjack.DealerHand(blackjack.Deck())
    
#Test dealing to varying number of players players
    #test if it can deal to one player
    def test_deal_to_one_players(self):
        player_num = 1
        player_cards = blackjack.deal_all_hands(player_num, self.deck)

        for cards in player_cards:
            for card in cards:
                self.assertIsInstance(card, blackjack.Card)

        self.assertEqual(len(player_cards), 1)
        self.assertEqual(len(self.deck.deck), 50)
    
    #Test if it can deal to 5 players
    def test_deal_to_five_players(self):
        player_num = 5
        player_cards = blackjack.deal_all_hands(player_num, self.deck)

        for cards in player_cards:
            for card in cards:
                self.assertIsInstance(card, blackjack.Card)

        self.assertEqual(len(player_cards), 5)
        self.assertEqual(len(self.deck.deck), 42)


    #Test if it will deal to no/0 players, This should fail
    def test_deal_to_no_players(self):
        player_num = 0
        player_cards = blackjack.deal_all_hands(player_num, self.deck)

        for cards in player_cards:
            for card in cards:
                self.assertIsInstance(card, blackjack.Card)

        self.assertEqual(len(player_cards), 0)
        self.assertEqual(len(self.deck.deck), 52)

    #Test if it will deal to above the max number of players, this should fail
    def test_deal_to_above_max_players(self):
        player_num = 9
        player_cards = blackjack.deal_all_hands(player_num, self.deck)

        for cards in player_cards:
            for card in cards:
                self.assertIsInstance(card, blackjack.Card)

        self.assertEqual(len(player_cards), 9)
        self.assertEqual(len(self.deck.deck), 34)

    #Test if it will deal to negative players, should fail
    def test_deal_to_negative_players(self):
        player_num = -1
        player_cards = blackjack.deal_all_hands(player_num, self.deck)

        for cards in player_cards:
            for card in cards:
                self.assertIsInstance(card, blackjack.Card)

        self.assertEqual(len(player_cards), -1)
        self.assertEqual(len(self.deck.deck), 38)

    #Test1
    def test_display_hand_of_current_turn_With_fifty_players(self):
        number_of_players = 50
        all_player_cards = blackjack.deal_all_hands(number_of_players, self.deck)

        for player_num in range(1, number_of_players + 1):
            current_players_cards = blackjack.get_current_players_cards(
                player_num, all_player_cards)

            # Player 1 cards should correspond to cards at index 0, player 2 at index, 1, etc..
            self.assertEqual(current_players_cards, all_player_cards[player_num - 1])

    #tets2
    def test_display_hand_of_current_turn_With_negative_players(self):
        number_of_players = -1
        all_player_cards = blackjack.deal_all_hands(number_of_players, self.deck)

        for player_num in range(1, number_of_players + 1):
            current_players_cards = blackjack.get_current_players_cards(
                player_num, all_player_cards)

            # Player 1 cards should correspond to cards at index 0, player 2 at index, 1, etc..
            self.assertEqual(current_players_cards, all_player_cards[player_num - 1])

    #test3
    def test_display_hand_of_current_turn_With_four_players(self):
        number_of_players = 4
        all_player_cards = blackjack.deal_all_hands(number_of_players, self.deck)

        for player_num in range(1, number_of_players + 1):
            current_players_cards = blackjack.get_current_players_cards(
                player_num, all_player_cards)

            # Player 1 cards should correspond to cards at index 0, player 2 at index, 1, etc..
            self.assertEqual(current_players_cards, all_player_cards[player_num - 1])

    #test4
    def test_display_hand_of_current_turn_With_nine_players(self):
        number_of_players = 9
        all_player_cards = blackjack.deal_all_hands(number_of_players, self.deck)

        for player_num in range(1, number_of_players + 1):
            current_players_cards = blackjack.get_current_players_cards(
                player_num, all_player_cards)

            # Player 1 cards should correspond to cards at index 0, player 2 at index, 1, etc..
            self.assertEqual(current_players_cards, all_player_cards[player_num - 1])
    
    #test5
    def test_display_hand_of_current_turn_With_5_players(self):
        number_of_players = 5
        all_player_cards = blackjack.deal_all_hands(number_of_players, self.deck)

        for player_num in range(1, number_of_players + 1):
            current_players_cards = blackjack.get_current_players_cards(
                player_num, all_player_cards)

            # Player 1 cards should correspond to cards at index 0, player 2 at index, 1, etc..
            self.assertEqual(current_players_cards, all_player_cards[player_num - 1])

    def test_add_new_card_to_hand(self):
        old_hand = self.dealer_hand.deal_hand()
        new_hand = blackjack.add_new_card_to_hand(old_hand, self.deck)
        new_card = list(set(new_hand) - set(old_hand)).pop()

        self.assertIsInstance(new_card, blackjack.Card)
        self.assertEqual(old_hand, list(set(new_hand) & set(old_hand)))
        self.assertEqual(len(new_hand) - len(old_hand), 1)




if __name__ == '__main__':
    unittest.main()
