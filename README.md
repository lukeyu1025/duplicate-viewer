# duplicate-viewer
An application to find duplicate files in a Synology NAS. The Synology Storage Analyzer program may miss some duplicate files as its main purpose is to analyze the NAS. This application provides a user-friendly interface to view and manage duplicate files listed in a CSV file generated from Synology's analysis, ensuring no duplicates are missed.
# Synology NAS Duplicate Finder

This application suite is designed to help users find and manage duplicate files in their Synology NAS. It consists of three Python scripts:

1. **cp.py**: Specify the folder to find duplicate files and the location for the output CSV file (`duplication_files.csv`).

2. **filter.py**: Filters `duplication_files.csv` based on user-defined criteria, generating `filtered_duplication_files.csv`.

3. **gui.py**: Provides a graphical user interface (GUI) for users to explore and manage duplicate files listed in `filtered_duplication_files.csv`.

## Usage

### 1. cp.py
- Run `cp.py`.
- Provide the folder path to find duplicate files.
- Specify the location to save the output CSV file.

### 2. filter.py
- Run `filter.py`.
- Provide the path to `duplication_files.csv`.
- Specify the location to save the filtered CSV file.

### 3. gui.py
- Run `gui.py`.
- Provide the path to `filtered_duplication_files.csv`.
- Explore and manage duplicate files using the graphical interface.

## Dependencies
- Python 3.x
- tkinter
- PIL (Python Imaging Library)
- pyautogui
- duplicates
