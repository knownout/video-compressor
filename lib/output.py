import re
from typing import Type


class FFmpegProcessOutput:
    """
    Ffmpeg process output parser
    """

    _parser: str

    # Current frame
    frame: int = 0

    # Frames processing count per second
    fps: int = 0

    # Video conversion speed
    speed: float = 0

    def __init__(self, parser="(frame=\s*\d+(?=\s*fps)|fps=\s*\d+|speed=\d\.?\d*(?=x))"):
        self._parser = parser

    def get(self):
        return [self.frame, self.fps, self.speed]

    @staticmethod
    def _replace(string: str, tail: str, converter: Type = int):
        """
        Internal method for replacing variable names in the string
        :param string: variable string
        :param tail: variable name
        :param converter: variable value parser
        :return: float or int
        """

        try:
            return converter(str(string).replace(tail, "").strip())
        except ValueError:
            return 0

    def parse(self, output: str):
        """
        Method for parsing variables from the process output string
        :param output: process output string
        :return: self
        """

        parsed = re.findall(self._parser, output)

        if len(parsed) > 0: self.frame = self._replace(parsed[0], "frame=")
        if len(parsed) > 1: self.fps = self._replace(parsed[1], "fps=")
        if len(parsed) > 2: self.speed = self._replace(parsed[2], "speed=", float)

        return self
