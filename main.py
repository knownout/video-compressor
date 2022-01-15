import os
import subprocess

import lib.utils as utils
from lib.output import FfmpegProcessOutput
from lib.progress import Progress


def main():
    target = input("Conversion target (file or directory): ")
    force = input("Force files conversion? (y/n): ").lower() == "y"

    files_list = utils.files_list(target)
    for file in files_list:
        convert(file, force)


def convert(file: str, force: bool):
    """
    File conversion function
    :param file: file path
    :param force: if True, removes output file if exist
    :return: void
    """
    codecs_blacklist = ["hevc"]
    info = utils.VideoInfo(file)

    output = FfmpegProcessOutput()
    outfile = f"{os.path.splitext(file)[0]}.mkv"

    if info.codec in codecs_blacklist:
        return

    if os.path.exists(outfile):
        if force:
            os.remove(outfile)
        else:
            return

    command = f"ffmpeg -i {file} -c:v libx265 -vtag hvc1 -c:a copy {outfile}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, stderr=subprocess.STDOUT,
                               universal_newlines=True)

    progress = Progress(target=file, percents=True, onfinish=f"+ Done")

    progress.show()
    for line in process.stdout:
        output.parse(line)
        left = round((info.frames - output.frame) / output.fps) if output.fps > 0 else 0

        progress.update(output.frame * 100 / info.frames, f", {left}s left" if left > 0 else "")

    progress.update(100)
    print("\n")


if __name__ == '__main__':
    main()
