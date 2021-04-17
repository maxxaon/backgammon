"""
Test.py
~~~~~~~~~~

Documentation test.

Authors:
- Maksim Marin 
- Roman Punkevich

:copyright: (c) 2021 by Marin and Punkevich
:license: MIT, see COPYING for more details.
"""


def my_sum(a, b):
    """
    Sum function

    :param a: left sum operand
    :param b: right sum operand
    :return: a+b
    """

    return a + b


def main():
    """Main application call"""
    print(my_sum(1, 2))


if __name__ == "__main__":
    main()

