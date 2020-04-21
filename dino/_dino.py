# -*- coding: utf-8 -*-
#
# Author: Felipe Junio da Rocha
# Date: 2020/04/13

from pyautogui import keyDown
from pyautogui import keyUp
from pyautogui import FAILSAFE
from brain import Brain


__all__ = ['Dino']


class Dino(Brain):

    def __init__(self) -> object:
        super(Dino, self).__init__(6, 6, 2, 2)
        self.__score: int = 0
        FAILSAFE = False

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, x) -> None:
        self.__score = x

    def jump(self, hold) -> None:

        if hold:
            keyDown('up')
        else:
            keyUp('up')

    def duck(self, hold) -> None:

        if hold:
            keyDown('down')
        else:
            keyUp('down')
