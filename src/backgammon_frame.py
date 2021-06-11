"""
backgammon_frame.py.

GUI Backgammon frame.
Authors:
- Maksim Marin
- Roman Punkevich

:copyright: (c) 2021 by Marin and Punkevich
:license: MIT, see COPYING for more details.
"""

import tkinter as tk
from tkinter import messagebox
import functools
from src.dice_frame import DiceFrame
from src.backgammon import Backgammon

import gettext

gettext.install("backgammon", localedir="translations")


class BackgammonFrame(tk.Frame):
    """GUI Backgammon frame class."""

    def __init__(self, master=None, backgammon=None):
        """
        Construct Backgammon frame class.

        :param master: parent frame
        :param backgammon: Backgammon backend object
        """
        super().__init__(master)

        self.backgammon = backgammon
        if self.backgammon is None:
            self.backgammon = Backgammon()

        self.rolled_numbers = []

        self.possible_moves = {}
        self.from_ind = None

        self.setupSpaces()

        self.createField()

        self.createDice()

        self.updateField()

    def setupSpaces(self):
        """Set all required spaces and configurations."""
        tk.Grid.rowconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 0, weight=1)

        self.grid(sticky="NEWS")

        self.topSpace = tk.Frame(self)
        self.topSpace.grid(sticky="NEWS")
        self.midSpace = tk.Frame(self)
        self.midSpace.grid(sticky="NEW")
        self.botSpace = tk.Frame(self)
        self.botSpace.grid(sticky="NEWS")

        self.columnconfigure(0, weight=1)
        for i in range(3):
            self.rowconfigure(i, weight=1)

    def createField(self):
        """Make field: add buttons."""
        self.places = []

        place_number_sep = Backgammon.PLACE_NUMBER // 2

        for i in range(place_number_sep):
            button = tk.Button(
                self.botSpace, text=str(i), command=functools.partial(self.makeTurn, i)
            )
            button.grid(row=0, column=i, sticky="NEWS")
            self.places.append(button)

        for i in range(place_number_sep, Backgammon.PLACE_NUMBER):
            button = tk.Button(
                self.topSpace, text=str(i), command=functools.partial(self.makeTurn, i)
            )
            button.grid(row=0, column=Backgammon.PLACE_NUMBER - i - 1, sticky="NEWS")
            self.places.append(button)

        self.botSpace.rowconfigure(0, weight=1)
        self.topSpace.rowconfigure(0, weight=1)
        for i in range(place_number_sep):
            self.botSpace.columnconfigure(i, weight=1, minsize=50)
            self.topSpace.columnconfigure(i, weight=1, minsize=50)

    def createDice(self):
        """Create Dice frame."""
        self.dice_frame = DiceFrame(self.midSpace)
        self.dice_frame.grid(row=0, column=0, sticky="NEWS")

    def checkNoMove(self):
        """Check whether current player doesn't have any moves."""
        turn_exists = False
        for i in range(Backgammon.PLACE_NUMBER):
            if len(self.backgammon.getMoves(i, self.rolled_numbers)) > 0:
                turn_exists = True
                break

        if not turn_exists:
            self.rolled_numbers = []
            self.endTurn()

    def updateField(self):
        """Update Field: color buttons."""
        array_repr = self.backgammon.getArrayRepr()
        for i in range(len(array_repr)):
            color = "gray"
            if array_repr[i] < 0:
                color = "black"
            elif array_repr[i] > 0:
                color = "white"
            self.places[i].configure(
                text=str(abs(array_repr[i])),
                background=color,
                foreground="red",
                activeforeground="blue",
                activebackground=color,
            )

        if len(self.rolled_numbers) > 0:
            self.checkNoMove()

    def endTurn(self):
        """End current turn to check for possible moves again."""
        self.possible_moves = {}
        if len(self.rolled_numbers) == 0:
            self.backgammon.changeTurn()
            self.dice_frame.makeActive()

        self.updateField()

    def makeTurn(self, place_ind):
        """
        Button callback. Try to find moves from this place.

        :param place_ind: button (place) index
        """
        if place_ind in self.possible_moves:
            numbers = self.possible_moves[place_ind]
            if self.backgammon.makeMove(self.from_ind, place_ind):
                messagebox.showinfo(_("You won!"))
                self.quit()
            for number in numbers:
                self.rolled_numbers.remove(number)

            self.endTurn()

            return
        else:
            self.possible_moves = {}
            self.updateField()

        if len(self.rolled_numbers) == 0:
            new_rolled_numbers = self.dice_frame.getRolledNumbers()
            if new_rolled_numbers is not None:
                self.rolled_numbers = new_rolled_numbers

            self.checkNoMove()

        self.possible_moves = self.backgammon.getMoves(place_ind, self.rolled_numbers)
        self.from_ind = place_ind

        for ind in self.possible_moves.keys():
            self.places[ind].config(background="green", activebackground="green")
