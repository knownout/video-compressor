import math
from os import path, listdir
from typing import Callable

import cv2


class TimeData:
    """
    Class for storing parsed time data
    """

    seconds: int = 0
    minutes: int = 0
    hours: int = 0

    def __init__(self, hours, minutes, seconds):
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours

    def get(self):
        """
        Method for getting parsed time data as an array
        :return: [hours, minutes, seconds]
        """
        return [self.hours, self.minutes, self.seconds]


def files_list(target: str, callback: Callable[[str], None] = None):
    """
    Function to get a list of files in a specific directory
    :param callback: fires when file added to the list
    :param target: path to the file or directory
    :return: list of files
    """
    files = list()

    # Return empty if path not exist
    if not path.exists(target):
        return files

    if path.isfile(target):
        files.append(target)
        return files

    elif path.isdir(target):
        for file in listdir(target):
            dir_target = path.join(target, file)
            if path.isfile(dir_target):
                files.append(dir_target)
                if callback: callback(file)

    return files


def sum_array(array: list):
    """
    Function for calculating the sum of array elements
    :param array: elements list
    :return: int
    """
    total = 0
    for i in array:
        total += i

    return total


def parse_time(seconds: int):
    """
    Convert seconds to TimeData object
    :param seconds: seconds count
    :return: TimeData
    """
    hours = math.floor(seconds / 60 / 60)
    minutes = math.floor(seconds / 60) - (hours * 60)
    seconds_left = seconds - hours * 60 * 60 - minutes * 60

    return TimeData(*[hours, minutes, seconds_left])


def format_time(value: int):
    """
    Format seconds into human readable string using parse_time
    :param value: seconds count
    :return: str
    """
    data = parse_time(value)
    strings = list(map(lambda x: "{:02d}".format(x), data.get()))
    formatted: list[str] = []

    if data.hours >= 1:
        formatted.append(f"{strings[0]}h")
    if data.minutes >= 1:
        formatted.append(f"{strings[1]}m")

    formatted.append(f"{strings[2]}s")

    if data.seconds == 0 and data.minutes == 0 and data.hours == 0:
        return "..."
    return " ".join(formatted).strip()


class VideoInfo:
    """
    Class for getting information about a specific video file
    """
    codec: str
    frames: int

    def __init__(self, target: str):
        if not path.exists(target) or not path.isfile(target):
            raise IOError("Not a file")

        video = cv2.VideoCapture(target)

        h = int(video.get(cv2.CAP_PROP_FOURCC))
        self.codec = chr(h & 0xff) + chr((h >> 8) & 0xff) + chr((h >> 16) & 0xff) + chr((h >> 24) & 0xff)
        self.frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
