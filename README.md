# ROM Playlist Generator

This script generates a playlist file (`.lpl`) for use with Retroarch. It supports handling both raw ROM files and ZIP-compressed ROM files. The script can generate CRC32 checksums for the ROM files, which can be used by Retroarch for things like game verification, metadata download, etc. While Retroarch does have this utility built in, instability can occur when using it (particularly with larger ROMsets).

Here be dragons- I haven't tested this extensively, and am not entirely sure how Retroarch's database matching works.

## Features

- **Supports Multiple File Types:** Process raw ROM files (e.g., `.iso`) and ZIP-compressed ROM files.
- **CRC32 Calculation:** Optionally calculate CRC32 checksums for ROM files.
- **User Customization:** Specify paths, file extensions, and database names via user input.

## Prerequisites

- Python 3.x
- `zlib` and `zipfile` libraries (included with Python)

## Getting Started

1. **Run the Script:** Open a terminal or command prompt and navigate to the directory where the script is located and run the following command: ```python PlaylistScript.py```
2. **Follow the Prompts**
3. **Place the playlist into** `Retroarch/playlists`
4. If games are not being detected, it is possible that the ROMs are corrupt. You can verify the integrity of the files by using tools such as [ROMCenter](https://romcenter.com/) or [RomVault](https://www.romvault.com/) to compare them against the No-Intro database which *should* match Retroarch's database.