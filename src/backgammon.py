"""
backgammon.py.

Backend Backgammon class.
Authors:
- Maksim Marin
- Roman Punkevich

:copyright: (c) 2021 by Marin and Punkevich
:license: MIT, see COPYING for more details.
"""


import math


class Backgammon:
    """Backgammon backend class."""

    class Turn:
        """Class to know who turns now."""

        WHITE = 1
        BLACK = -1

    PLACE_NUMBER = 24
    CHECKERS_NUMBER = 15

    START_POS_WHITE = 0
    START_POS_BLACK = PLACE_NUMBER // 2

    EXIT_RANGES = {
        Turn.WHITE: [PLACE_NUMBER - 6, PLACE_NUMBER - 1],
        Turn.BLACK: [START_POS_BLACK - 6, START_POS_BLACK - 1],
    }

    def __init__(self, init_array=None, init_dict=None, turn=Turn.WHITE):
        """
        Construct Backgammon.

        :param init_array: field as array
        :param init_dict: field as dict
        """
        self.turn = turn

        self.is_start_used = False

        self.is_exit_state = {self.Turn.WHITE: False, self.Turn.BLACK: False}

        if init_array is None and init_dict is None:
            init_dict = {
                0: self.CHECKERS_NUMBER,
                self.START_POS_BLACK: -self.CHECKERS_NUMBER,
            }

        if init_dict is not None:
            self.array_repr = [0] * self.PLACE_NUMBER
            for k, v in init_dict.items():
                self.array_repr[k] = v
        else:
            self.array_repr = init_array

    def getArrayRepr(self):
        """Get backgammon field state as python array."""
        return self.array_repr

    def changeTurn(self):
        """Change turn."""
        self.turn *= -1

        self.is_start_used = False

    def isStartPlace(self, place_ind):
        """
        Check whether it is start place for current gamer.

        :param place_ind: place id
        :return: bool
        """
        return (place_ind == self.START_POS_WHITE and self.turn == self.Turn.WHITE) or (
            place_ind == self.START_POS_BLACK and self.turn == self.Turn.BLACK
        )

    def isEndMove(self, to_ind):
        """
        Check whether it is last move for the checker.

        :param to_ind: place id where we put it
        :return: bool
        """
        if not self.is_exit_state[self.turn]:
            return False

        if self.turn == self.Turn.WHITE:
            return to_ind < self.PLACE_NUMBER - 6
        else:
            return to_ind >= self.START_POS_BLACK or to_ind < self.START_POS_BLACK - 6

    def isPlaceForMe(self, to_ind):
        """
        Check whether we can put checker here.

        :param to_ind: place id where we put it
        :return: bool
        """
        return (
            math.copysign(1, self.array_repr[to_ind]) == self.turn
            or self.array_repr[to_ind] == 0
        )

    def isMovePossible(self, from_ind, to_ind):
        """
        Check whether move from from_ind to to_ind possible.

        :param from_ind: place id where we take checker
        :param to_ind: place id where we put it
        :return: bool
        """
        if self.turn == self.Turn.WHITE:
            if self.is_exit_state[self.turn] is True:
                return self.isEndMove(to_ind) or self.isPlaceForMe(to_ind)
            else:
                return not (to_ind < from_ind) and self.isPlaceForMe(to_ind)
        else:
            if self.is_exit_state[self.turn] is True:
                return self.isEndMove(to_ind) or self.isPlaceForMe(to_ind)
            else:
                return not (
                    from_ind < self.START_POS_BLACK and to_ind >= self.START_POS_BLACK
                ) and self.isPlaceForMe(to_ind)

    def getMoves(self, place_ind, rolled_numbers):
        """
        Get possible moves from place_ind with rolled_numbers.

        :param from_ind: place id where we take checker
        :param rolled_numbers: numbers that we currently have in dice
        :return: dict {to_ind: [numbers], ...}
        """
        self.updateExitState()

        if (
            self.array_repr[place_ind] == 0
            or math.copysign(1, self.array_repr[place_ind]) != self.turn
        ):
            return {}
        if self.isStartPlace(place_ind) and self.is_start_used:
            return {}

        moves = {}
        for number in sorted(rolled_numbers):
            ind = (place_ind + number) % self.PLACE_NUMBER
            key = ind if not self.isEndMove(ind) else place_ind
            if self.isMovePossible(place_ind, ind) and key not in moves:
                moves[key] = [number]

        if len(rolled_numbers) == 2:
            ind = (place_ind + sum(rolled_numbers)) % self.PLACE_NUMBER
            key = ind if not self.isEndMove(ind) else place_ind
            if self.isMovePossible(place_ind, ind) and key not in moves:
                moves[key] = rolled_numbers.copy()
        elif len(rolled_numbers) >= 3:
            for cnt in range(2, len(rolled_numbers) + 1):
                ind = (place_ind + cnt * rolled_numbers[0]) % self.PLACE_NUMBER
                key = ind if not self.isEndMove(ind) else place_ind
                if self.isMovePossible(place_ind, ind) and key not in moves:
                    moves[key] = [rolled_numbers[0]] * cnt

        return moves

    def updateExitState(self):
        """Update exit states for both players."""
        min_exit_ind, max_exit_ind = self.EXIT_RANGES[self.turn]
        self.is_exit_state[self.turn] = True
        for i, val in enumerate(self.array_repr):
            if (
                val != 0
                and math.copysign(1, val) == self.turn
                and (i < min_exit_ind or i > max_exit_ind)
            ):
                self.is_exit_state[self.turn] = False

    def getWinStatus(self):
        """
        Get whether current player won.

        :return: bool win_status
        """
        win_state = True
        for i, val in enumerate(self.array_repr):
            if val != 0 and math.copysign(1, val) == self.turn:
                win_state = False
        return win_state

    def makeMove(self, from_ind, to_ind):
        """
        Make move.

        :param from_ind: place id where we take checker
        :param to_ind: place id where we put it
        :return: bool win_status
        """
        self.array_repr[from_ind] -= self.turn

        if to_ind != from_ind:
            self.array_repr[to_ind] += self.turn

        if self.isStartPlace(from_ind):
            self.is_start_used = True

        self.updateExitState()

        return self.getWinStatus()
