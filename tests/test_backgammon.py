"""
test_backgammon.py
~~~~~~~~~~
Tests for Backgammon class.
Authors:
- Maksim Marin
- Roman Punkevich
:copyright: (c) 2021 by Marin and Punkevich
:license: MIT, see COPYING for more details.
"""


import unittest

from src.backgammon import Backgammon


class TestStringMethods(unittest.TestCase):
    def test_is_end_move(self):
        backgammon = Backgammon(turn=Backgammon.Turn.WHITE)

        self.assertFalse(backgammon.isEndMove(3))

        backgammon.is_exit_state[Backgammon.Turn.WHITE] = True

        self.assertTrue(backgammon.isEndMove(3))

    def test_is_move_possible(self):
        backgammon = Backgammon(turn=Backgammon.Turn.WHITE)

        self.assertFalse(backgammon.isMovePossible(20, 5))
        self.assertTrue(backgammon.isMovePossible(1, 5))

        backgammon.is_exit_state[Backgammon.Turn.WHITE] = True

        self.assertTrue(backgammon.isMovePossible(20, 5))

    def test_get_moves(self):
        backgammon = Backgammon(turn=Backgammon.Turn.WHITE)

        self.assertEqual(backgammon.getMoves(0, [3, 5]), {3: [3], 5: [5], 8: [3, 5]})

        backgammon = Backgammon(turn=Backgammon.Turn.WHITE, init_dict={20: 1})

        self.assertEqual(backgammon.getMoves(20, [3, 5]), {23: [3], 20: [5]})

    def test_is_start_place(self):
        backgammon = Backgammon(turn=Backgammon.Turn.WHITE)

        self.assertTrue(backgammon.isStartPlace(0))
        self.assertFalse(backgammon.isStartPlace(6))

        backgammon.changeTurn()

        self.assertFalse(backgammon.isStartPlace(0))
        self.assertTrue(backgammon.isStartPlace(12))

    def test_get_win_status(self):
        backgammon = Backgammon(turn=Backgammon.Turn.WHITE, init_dict={20: 1})

        self.assertFalse(backgammon.getWinStatus())

        backgammon.makeMove(20, 20)

        self.assertTrue(backgammon.getWinStatus())
