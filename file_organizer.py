"""
File Organizer
--------------
Sorts all files in a folder into sub-folders based on their extension.
For example: photo.jpg -> Images/photo.jpg

Usage:
    python file_organizer.py                  # organize the default folder
    python file_organizer.py /path/to/folder  # organize a specific folder
    python file_organizer.py --dry-run        # only show what would happen
"""

import os
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------

# Folder to organize if none is given on the command line
DEFAULT_FOLDER = Path.home() / "Downloads"

# Which extension goes into which folder
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".odt"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Audio": [".mp3", ".wav", ".m4a", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json"],
    "Installers": [".exe", ".msi", ".deb", ".dmg", ".apk"],
}

# Anything that does not match the table above goes here
OTHER_FOLDER = "Others"


# ---------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------

def get_category(file_path):
    """Return the folder name this file belongs to, based on its extension."""
    extension = file_path.suffix.lower()

    for category, extension_list in CATEGORIES.items():
        if extension in extension_list:
            return category

    return OTHER_FOLDER


def build_safe_destination(destination_folder, file_name):
    """
    Return a destination path that does not overwrite an existing file.
    If report.pdf already exists, this returns report_1.pdf, report_2.pdf, etc.
    """
    destination = destination_folder / file_name

    if not destination.exists():
        return destination

    stem = Path(file_name).stem
    suffix = Path(file_name).suffix
    counter = 1

    while destination.exists():
        destination = destination_folder / f"{stem}_{counter}{suffix}"
        counter += 1

    return destination


def organize(folder, dry_run=False):
    """Move every file in the folder into its category sub-folder."""
    folder = Path(folder)

    if not folder.is_dir():
        print(f"Error: '{folder}' is not a valid folder.")
        return

    print(f"Organizing: {folder}")
    if dry_run:
        print("DRY RUN - nothing will actually be moved.\n")

    moved_count = 0
    skipped_count = 0

    # Only look at items directly inside the folder, not inside sub-folders
    for item in folder.iterdir():

        # Skip sub-folders - we only move files
        if item.is_dir():
            continue

        # Skip hidden files such as .gitignore
        if item.name.startswith("."):
            skipped_count += 1
            continue

        category = get_category(item)
        destination_folder = folder / category
        destination = build_safe_destination(destination_folder, item.name)

        print(f"  {item.name}  ->  {category}/{destination.name}")

        if not dry_run:
            # Create the category folder only when it is actually needed
            destination_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))

        moved_count += 1

    print(f"\nDone. {moved_count} file(s) organized, {skipped_count} skipped.")


# ---------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------

def main():
    arguments = sys.argv[1:]

    dry_run = "--dry-run" in arguments
    if dry_run:
        arguments.remove("--dry-run")

    target_folder = arguments[0] if arguments else DEFAULT_FOLDER

    organize(target_folder, dry_run=dry_run)


if __name__ == "__main__":
    main()
