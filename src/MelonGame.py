# -*- coding: utf-8 -*-
import csv

import globals
import numpy as np


def remove_empty(list_, item=""):
    return [i for i in list_ if i != item]


def clean_row(list_):
    row = ""
    for item in list_:
        if item in globals.IDS:
            row += f"<:{item}:{globals.IDS[item]}>"
        else:
            row += f":{item}:"
    if row[-2] == ":":
        return row[:-2]

    return row


class Player(object):
    def __init__(self):
        self._health = 40
        self._mana = 30
        # Regens 5 per turn
        self._stamina = 20
        self._player_abilities = None

    @property
    def player_abilities(self):
        if self._player_abilities is None:
            return "No abilities set!"
        return ", ".join(self._player_abilities)

    @player_abilities.setter
    def player_abilities(self, abilities):
        for i, j in zip(abilities, globals.Abilities):
            if i not in globals.Abilities[j]:
                raise ValueError(f"Invalid player ability {j}: {i}")
        self._player_abilities = abilities


# class Computer(object):


class Melon(object):
    def __init__(self):
        self.board_dim = (18, 14)
        self._init_board()
        self.Player = Player()

    def _init_board(self, filename="board.txt"):
        self.board = np.zeros((self.board_dim), dtype="<U25")
        with open(filename, "r") as f:
            reader = csv.reader(f, delimiter=":")
            for X, row in enumerate(reader):
                row = remove_empty(row)
                for Y, item in enumerate(row):
                    self.board[X][Y] = item
