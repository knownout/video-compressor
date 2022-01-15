# Python H.265 videos compressor

<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/re-knownout/video-compressor"> <img alt="GitHub package.json version" src="https://img.shields.io/github/package-json/v/re-knownout/video-compressor"> <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/re-knownout/video-compressor"> <img alt="GitHub" src="https://img.shields.io/github/license/re-knownout/video-compressor">

Python console utility to compress video files by converting them to H.265 codec using FFmpeg. Supports both command
line arguments and user input _(user input is only available if not all variables are covered by command line
arguments)_

Tested only on Windows 10 _(I think it works in ubuntu too, but may not resolve some input paths)_

There may be some bugs with the rendering of the progress bar because I'm not too good with the command line cursor in
python.
_(where is my SetCursorPosition from C#?)_

### File compression time

A speed test was carried out for compressing video files of approximately **55mb in size**, with the **AVC2** codec and
a duration of about **4 minutes**. AMD Ryzen 7 3700x 8/16 used as CPU

| Threads | Files | Elapsed time | Description                                                                                                    |
|---------|-------|--------------|----------------------------------------------------------------------------------------------------------------|
| 1       | 4     | 02m 27s      | Just a single thread compression                                                                               |
| 2       | 4     | 01m 46s      | Threads covered half of files count                                                                            |
| 4       | 4     | 01m 36s      | Threads covered all provided files                                                                             |
| 16      | 4     | 01m 35s      | It does not make sense to specify more threads than files in the source, extra threads will not be used anyway |

The table below shows the percentage of compression speed for different number of streams _(single-thread mode and
multi-thread modes)_

| Base                 | Comparison           | Result |
|----------------------|----------------------|--------|
| Single thread        | Multiple threads (4) | +34%   |
| Single thread        | Multiple threads (2) | +28%   |
| Multiple threads (2) | Multiple threads (4) | +13%   |

As you can see, in any case use the multiple threads provides approximately 28% speed increase, if used more threads the
speed also increases, however, with each new thread, the percentage drops

### Command line arguments

To automate the use of this utility, command line arguments are provided that allow you to disable manual entry of
specified variables.

| Argument  | Shortcut | Type | Description                                                       |
|-----------|----------|------|-------------------------------------------------------------------|
| --force   | -f       | bool | Force compress files even if files already has compressed version |
| --input   | -i       | str  | Target directory or file                                          |
| --output  | -o       | str  | Relative path for compressed files                                |
| --threads | -t       | int  | Threads count for compression                                     |

re-knownout - https://github.com/re-knownout/
<br>knownout@hotmail.com