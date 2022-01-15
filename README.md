# video-compressor

<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/re-knownout/video-compressor"> <img alt="GitHub package.json version" src="https://img.shields.io/github/package-json/v/re-knownout/video-compressor"> <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/re-knownout/video-compressor"> <img alt="GitHub" src="https://img.shields.io/github/license/re-knownout/video-compressor">

Simple python3 console program for converting videos using FFmpeg to the H.265 codec

### Files conversion time

Conversion processed with Ryzen 7 3700x 8/16 stock and MP4 AVC2 ~4:10 ~55mb video files

| Threads | Files | Elapsed time |
|---------|-------|--------------|
| 1       | 4     | 02m 27s      |
| 2       | 4     | 01m 46s      |
| 4       | 4     | 01m 36s      |
| 16      | 4     | 01m 35s      |

| Base             | Comparison       | Result |
|------------------|------------------|--------|
| Single thread    | Multi thread (4) | +34%   |
| Multi thread (2) | Multi thread (4) | +13%   |


