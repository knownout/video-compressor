import math


class Progress:
    """
    Class for creating simple progress bars
    """

    _tiles: int
    _target: str
    _percents: bool
    _onfinish: str

    def __init__(self, tiles=20, target="", percents=False, onfinish: str = ""):
        self._tiles = tiles
        self._target = target
        self._percents = percents
        self._onfinish = onfinish

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

        if tiles == self._tiles and len(self._onfinish) > 0:
            print("\r", end="")
            for i in range(40):
                self._print(" ")
            print("\r", end="")

            print(self._onfinish, end="")
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
        print("\r", end="")
        for i in range(40):
            self._print(" ")
        print("\r", end="")

        return self._render(progress, info)
