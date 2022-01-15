from os import path, listdir

import cv2


def files_list(target: str):
    files = list()
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

    return files


class VideoInfo:
    codec: str
    frames: int

    def __init__(self, target: str):
        if not path.exists(target) or not path.isfile(target):
            raise IOError("Not a file")

        video = cv2.VideoCapture(target)

        h = int(video.get(cv2.CAP_PROP_FOURCC))
        self.codec = chr(h & 0xff) + chr((h >> 8) & 0xff) + chr((h >> 16) & 0xff) + chr((h >> 24) & 0xff)
        self.frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
