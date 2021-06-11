"""
dice_frame.py.

GUI Dice frame.
Authors:
- Maksim Marin
- Roman Punkevich

:copyright: (c) 2021 by Marin and Punkevich
:license: MIT, see COPYING for more details.
"""


import tkinter as tk
import random
import time

import gettext

gettext.install("backgammon", localedir="translations")


class DiceFrame(tk.Frame):
    """GUI Dice frame class."""

    def __init__(self, master=None):
        """
        Construct Dice frame class.

        :param master: parent frame
        """
        super().__init__(master)

        self.rolled_numbers = None

        self.createFrame()

    def createFrame(self):
        """Create all parts of this frame: button and labels."""
        self.grid(sticky="NEWS")
        self.generate_button = tk.Button(
            self, text=_("Roll the dice"), command=self.roll
        )
        self.generate_button.grid(row=0, column=0, sticky="NEWS")
        self.dice_labels = []
        for i in range(2):
            self.dice_labels.append(tk.Label(self, text="0"))
        for i in range(len(self.dice_labels)):
            self.dice_labels[i].grid(row=0, column=i + 1, sticky="NEWS")

        for i in range(3):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=1)

    def roll(self):
        """Generate to random numbers from 1 to 6."""
        self.generate_button.configure(state="disabled")
        for i in range(10):
            numbers = []
            for i in range(2):
                numbers.append(random.randint(1, 6))
            for i in range(2):
                self.dice_labels[i].config(text=str(numbers[i]))

            if i != 9:
                self.update_idletasks()
                time.sleep(0.1)

        if numbers[0] == numbers[1]:
            numbers += numbers

        self.rolled_numbers = numbers

    def makeActive(self):
        """Make generate button active."""
        for i in range(2):
            self.dice_labels[i].config(text="0")
        self.generate_button.configure(state="normal")

    def getRolledNumbers(self):
        """
        Get what numbers we have generated.

        :return: rolled_numbers array
        """
        res = self.rolled_numbers
        self.rolled_numbers = None
        return res
