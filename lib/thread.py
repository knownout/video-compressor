import threading

import lib.utils as utils


class FileInfo:
    """
    Class for storing data about files compression progress
    """

    # Already processed frames count
    frames: int = 0

    def update(self, frames):
        """
        Method for setting processed frames count
        :param frames: frames count
        :return: self
        """
        self.frames = frames
        return self

    def get(self):
        """
        Method for getting processed frames count
        :return: int
        """
        return self.frames


class ThreadInfo:
    """
    Class for storing information about specific thread
    """

    # Thread name
    name: str

    # Thread frames processing count
    fps: int = 0

    # Thread processing speed
    speed: float = 0

    # Thread instance
    thread: threading.Thread

    def __init__(self, thread: threading.Thread, name: str):
        self.thread = thread
        self.name = name

    def update(self, fps: int, speed: float):
        """
        Method for updating fps and speed values
        :param fps: frames per second
        :param speed: compression speed
        :return: self
        """
        self.fps = fps
        self.speed = speed
        return self


class ThreadsInfo:
    """
    Class for generating average information about all
    provided threads wrapped with class ThreadInfo
    """

    # Average frames per second
    fps: int

    # Average conversion speed
    speed: float

    def __init__(self, *threads: ThreadInfo):
        # fps variables from all threads
        fps = []

        # speed variables from all threads
        speed = []

        for thread in threads:
            fps.append(thread.fps)
            speed.append(thread.speed)

        # Calculate average values
        self.fps = round(utils.sum_array(fps) / len(fps))
        self.speed = round(utils.sum_array(speed) / len(speed), 2)
