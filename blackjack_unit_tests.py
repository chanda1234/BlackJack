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
        self.assertEqual(len(self.deck.deck), 52)

    @mock.patch('blackjack.random')
    def test_call_shuffle_on_deck(self, mock_random):
        self.assertFalse(mock_random.shuffle.called)
        blackjack.Deck()
        self.assertTrue(mock_random.shuffle.called)

    def test_check_deal_card_returns_card(self):
        card = self.deck.deal_card()
        self.assertIsInstance(card, blackjack.Card)
        self.assertEqual(len(self.deck.deck), 51)

class testHandClass(unittest.TestCase):

    def setUp(self):
        self.hand = blackjack.Hand(blackjack.Deck())
        self.dealer_hand = blackjack.DealerHand(blackjack.Deck())
        self.example_hard_cards = [blackjack.Card(
            13, 'Diamonds'), blackjack.Card(4, 'Clubs')]
        self.example_soft_cards = [blackjack.Card(1, 'Ace'),
                                   blackjack.Card(6, 'Six')]
        self.example_blackjack_cards = [blackjack.Card(1, 'Ace'),
                                        blackjack.Card(10, 'King')]

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

    def test_dealer_should_hit(self):
        # Lowest possible score on a hand is two points.
        for total in range(2, 21):
            if total < 17:
                self.assertTrue(self.dealer_hand.dealer_should_hit(total))
            else:
                self.assertFalse(self.dealer_hand.dealer_should_hit(total))


if __name__ == '__main__':
    unittest.main()
