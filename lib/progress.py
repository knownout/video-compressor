import math
from typing import Callable


class Progress:
    """
    Class for creating simple progress bars
    """

    _tiles: int
    _target: str
    _percents: bool

    _callback: Callable

    def __init__(self, tiles=20, target="", percents=False, callback: Callable = None):
        self._tiles = tiles
        self._target = target
        self._percents = percents
        self._callback = callback

    @staticmethod
    def _print(*string: str):
        """
        Internal method for printing stripped tuples without new line
        :param string: values to be printed
        :return: void
        """
        print(" ".join(string).strip(), end="")

    def _render(self, progress: float, info: str = ""):
        """
        Internal method for rendering progress bar
        :param progress: current progress percent
        :param info: progress info
        :return: self
        """
        tiles = (progress * self._tiles) / 100
        self._print("[")

        for i in range(self._tiles):
            print("▪" if i == math.ceil(tiles) else "■" if i < tiles else " ", end="")

        self._print("]", "".join(["{:.2f}".format(round(progress, 2)) + "%" if self._percents else "", info]))

        # Check if completed and has callback
        if tiles == self._tiles and self._callback:
            # Clean console before next output
            print("\r", end="")
            for i in range(40):
                self._print(" ")
            print("\r", end="")

            self._callback()
        return self

    def show(self, info: str = ""):
        """
        Method for first progress bar rendering
        :param info: progress info
        :return: self
        """
        print(self._target, end="\n")
        return self._render(0, info)

    def update(self, progress: float, info: str = ""):
        """
        Method for updating progress bar without re-render
        :param progress: current progress percent
        :param info: progress info
        :return: self
        """

        # Clean console before next output
        print("\r", end="")
        for i in range(40):
            self._print(" ")
        print("\r", end="")

        return self._render(progress, info)

    def set_callback(self, callback: Callable):
        """
        Method for updating callback (fires when progress get to 100 percents)
        :param callback: Callable
        :return:
        """
        self._callback = callback
