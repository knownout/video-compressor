import os
import subprocess
import threading
import time

import lib.utils as utils
from lib.output import FFmpegProcessOutput
from lib.progress import Progress
from lib.thread import ThreadInfo, ThreadsInfo, FileInfo


class Main:
    # Files list
    files: list[str] = []

    # Progress bar instance
    progress = Progress(percents="True")

    """ User-defined variables """

    # Remove files named like output file if exist
    force: bool = False

    # Count of the threads to be created
    threads: int = os.cpu_count()

    """ Thread information storages """

    # Threads info storage
    threads_info: dict[int, ThreadInfo] = {}

    # Files info storage
    files_info: dict[str, FileInfo] = {}

    """ Internal program data """

    # Total frames in the provided files
    frames: int = 0

    # Conversion start time
    start_time: float

    def callback(self):
        """
        Method to be run when all threads have finished compressing files
        :return: None
        """
        print(f"+ {len(self.files)} file(s) converted")
        print(f"Elapsed time: {utils.format_time(round(time.time() - self.start_time))}")
        # exit(0)

    def __init__(self):
        # Target directory or file
        target = input("Conversion target (file or directory): ")

        # Try to read threads count from the user or set default value
        try:
            value = input(f"Threads limit ({self.threads}): ")
            parsed_value = int(value) if len(value.strip()) > 0 else self.threads
            if parsed_value > os.cpu_count():
                raise ValueError(f"Invalid threads count ({parsed_value}), only {os.cpu_count()} threads available")
            if parsed_value < 1:
                raise ValueError(f"Threads count can not be lower than 1")

        except ValueError as e:
            print(e)
            print(f"Invalid value for threads limit, set to {self.threads}")

        # Allow script to remove old output files if exist
        self.force = input("Force files conversion? (y/n): ").lower() == "y"

        """ Data processing """

        # Callback for utils.files_list function
        def update_files_info(file: str):
            info = utils.VideoInfo(file)

            self.files_info[file] = FileInfo()
            self.frames += info.frames

        # Get target path files list
        self.files = utils.files_list(target, update_files_info)

        # Update progress callback
        self.progress.set_callback(self.callback)

        # Split files list to chunks
        chunks = self.split_files()

        # Update compression start time
        self.start_time = time.time()

        # Show progress bar
        self.progress.show()

        # Create threads
        for key, chunk in enumerate(chunks):
            if len(chunk) == 0: continue

            thread = threading.Thread(target=self.compress, args=(chunk, key))
            self.threads_info[key] = ThreadInfo(thread, f"Thread {key + 1}")
            thread.start()

    def split_files(self):
        """
        Method for splitting files list to the chunks
        :return: list[list[str]]
        """

        # Blacklisted video file codecs
        codecs_blacklist = ["hevc"]

        # Chunks list structure
        chunks = [[] for _ in range(self.threads)]

        # The index of the chunk to add to
        write_chunk = 0

        for file in self.files:
            info = utils.VideoInfo(file)
            if info.codec in codecs_blacklist:
                continue

            chunks[write_chunk].append(file)

            if write_chunk >= len(chunks) - 1:
                write_chunk = 0
            else:
                write_chunk += 1

        return chunks

    def compress(self, chunk: list[str], thread: int):
        """
        Method for compressing list of the files
        :param chunk: files list
        :param thread: compression thread index
        :return: None
        """

        for file in chunk:
            # Process output parser instance
            output = FFmpegProcessOutput()

            # Output file name
            outfile = f"{os.path.splitext(file)[0]}.mkv"

            # Check if output file path exist and delete if allowed
            if os.path.exists(outfile):
                if self.force:
                    os.remove(outfile)
                else:
                    return

            # Compression command
            command = f"ffmpeg -i {file} -c:v libx265 -vtag hvc1 -c:a copy {outfile}"

            # Compression process
            process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

            # Read process stdout
            for line in process.stdout:
                # Parse process output
                output.parse(line)

                # Update threads and files info based on the output
                self.threads_info[thread].update(output.fps, output.speed)
                self.files_info[file].update(output.frame)

                # Get average threads info and processed frames count
                info = ThreadsInfo(*self.threads_info.values())
                frames = utils.sum_array(list(map(lambda key: self.files_info[key].frames, self.files_info.keys())))

                # Calculate total progress in percents
                percents = frames * 100 / self.frames

                # Calculate time left (not very accurate)
                # Todo: there are some properties of time and speed in the output, maybe i should use them
                left = utils.format_time(round(((self.frames - frames) / info.fps) if info.fps > 0 else 0))

                # Get elapsed time in human-readable format
                elapsed = utils.format_time(round(time.time() - self.start_time))

                # Update progress
                self.progress.update(percents, f", {frames} of {self.frames} frames, "
                                     + f"{left} left, {elapsed} elapsed")


if __name__ == '__main__':
    Main()
