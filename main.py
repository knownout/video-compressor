import os
import platform
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

    # Compressed files output directory
    output: str = ""

    # Count of the threads to be created
    threads: int = os.cpu_count()

    """ Thread information storages """

    # Threads info storage
    threads_info: dict[int, ThreadInfo] = {}

    # Files info storage
    files_info: dict[str, FileInfo] = {}

    # Blacklisted video file codecs
    codecs_blacklist = ["hevc"]

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

        elapsed = utils.format_time(round(time.time() - self.start_time))

        print(f"+ {len(self.files)} file(s) compressed")

        if elapsed == "...":
            print("All files are skipped because they have already been converted")
        else:
            print(f"Elapsed time: {elapsed}")

        exit(0)

    def __init__(self):
        # Target directory or file
        target = input("Conversion target (file or directory): ")

        """ Data processing """

        # Callback for utils.files_list function
        def update_files_info(file: str):
            info = utils.VideoInfo(file)

            if info.codec in self.codecs_blacklist:
                return False

            self.files_info[file] = FileInfo()
            self.frames += info.frames
            return True

        # Get target path files list
        self.files = utils.files_list(target, update_files_info)

        # Set default threads count
        self.threads = self.threads if self.threads <= len(self.files) else len(self.files)

        """ Variables processing (2) """

        # Try to read threads count from the user or set default value
        try:
            value = input(f"Threads limit ({self.threads}): ")
            parsed_value = int(value) if len(value.strip()) > 0 else self.threads
            if parsed_value > os.cpu_count():
                raise ValueError(f"Invalid threads count ({parsed_value}), only {os.cpu_count()} threads available")
            if parsed_value < 1:
                raise ValueError(f"Threads count can not be lower than 1")

            self.threads = parsed_value

        except ValueError as e:
            print(e)
            print(f"Invalid value for threads limit, set to {self.threads}")

        if self.threads < os.cpu_count() and self.threads < len(self.files):
            print(f"\n! You have only specified {self.threads} threads to use, but there are {len(self.files)} " +
                  f"files and your CPU has {os.cpu_count()} threads\n")

        if self.threads > len(self.files):
            print(f"\n! You have specified to use more threads than files in a directory, " +
                  f"only {len(self.files)} threads will be used\n")

        # Rewrite files output directory
        rewrite_output = input("Relative path for the output files ( ): ")
        if os.path.isdir(target) and os.path.isdir(os.path.join(target, rewrite_output)):
            self.output = rewrite_output
        else:
            print(f"Invalid relative path, set to default (./)")

        # Allow script to remove old output files if exist
        self.force = input("Force files conversion? (y/n): ").lower() == "y"

        """ Data processing (2) """

        # Update progress callback
        self.progress.set_callback(self.callback)

        # Split files list to chunks
        chunks = self.split_files()

        # Update compression start time
        self.start_time = time.time()

        print(f"\nCompressing {len(self.files)} file(s) with {self.threads} threads")
        print(f"CPU: {platform.processor()}")

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

        # Chunks list structure
        chunks = [[] for _ in range(self.threads)]

        # The index of the chunk to add to
        write_chunk = 0

        for file in self.files:
            info = utils.VideoInfo(file)
            if info.codec in self.codecs_blacklist:
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
            command = f"ffmpeg -i {file} -c:v libx265 -vtag hvc1 -c:a copy {os.path.join(self.output, outfile)}"

            # Compression process
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       bufsize=1, universal_newlines=True)

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

                active_threads = len(list(filter(
                    lambda y: y.is_alive(), map(lambda x: x.thread, self.threads_info.values()))
                ))
                # Update progress
                self.progress.update(percents, f", {frames} of {self.frames} frames, "
                                     + f"{left} left, {elapsed} elapsed, {active_threads}/{self.threads} threads")


if __name__ == '__main__':
    main = Main()

    if time.time() - main.start_time > 1:
        main.progress.update(100)
