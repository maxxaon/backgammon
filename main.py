"""
main.py.

Run backgammon app.
Authors:
- Maksim Marin
- Roman Punkevich

:copyright: (c) 2021 by Marin and Punkevich
:license: MIT, see COPYING for more details.
"""


import sys
from src.backgammon_frame import BackgammonFrame
from src.backgammon import Backgammon


import gettext

gettext.install("backgammon", localedir="translations")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test-end":
        app = BackgammonFrame(
            backgammon=Backgammon(init_dict={20: 2, 22: 2, 16: 1, 8: -2, 9: -2, 5: -1})
        )
    elif len(sys.argv) > 1 and sys.argv[1] == "test-win":
        app = BackgammonFrame(
            backgammon=Backgammon(init_dict={22: 1, 8: -2, 9: -2, 5: -1})
        )
    else:
        app = BackgammonFrame()
    app.master.title(_("Backgammon"))
    app.master.geometry("1500x1000")
    app.mainloop()
