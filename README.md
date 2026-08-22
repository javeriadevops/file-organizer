# File Organizer

A Python script that cleans up a messy folder by moving every file into a
sub-folder based on its file type. Point it at your Downloads folder and it
turns a pile of 200 random files into neat `Images/`, `Documents/`, `Videos/`
folders in a few seconds.

---

## What it does

- Reads every file in the target folder
- Decides its category from the file extension
- Creates the category folder (only if it is actually needed)
- Moves the file there
- Never overwrites anything &mdash; a duplicate `report.pdf` becomes `report_1.pdf`
- Leaves sub-folders and hidden files alone

### Categories

| Folder | Extensions |
|---|---|
| `Images` | jpg, jpeg, png, gif, bmp, webp, svg |
| `Documents` | pdf, doc, docx, txt, ppt, pptx, odt |
| `Spreadsheets` | xls, xlsx, csv |
| `Videos` | mp4, mkv, avi, mov, wmv |
| `Audio` | mp3, wav, m4a, aac, flac |
| `Archives` | zip, rar, 7z, tar, gz |
| `Code` | py, js, html, css, java, cpp, c, json |
| `Installers` | exe, msi, deb, dmg, apk |
| `Others` | everything else |

---

## Requirements

- Python 3.7 or newer
- No external libraries &mdash; standard library only

---

## How to run

```bash
# Clone the repository
git clone https://github.com/<your-username>/file-organizer.git
cd file-organizer

# Preview first - this shows what would move, without moving anything
python file_organizer.py --dry-run

# Organize the default folder (your Downloads)
python file_organizer.py

# Or organize any folder you want
python file_organizer.py /path/to/some/folder
```

> **Tip:** always run `--dry-run` the first time on a new folder, so you can see
> the plan before any file is actually moved.

---

## Sample output

```
Organizing: /home/user/Downloads
DRY RUN - nothing will actually be moved.

  invoice.pdf        ->  Documents/invoice.pdf
  screenshot.png     ->  Images/screenshot.png
  setup.exe          ->  Installers/setup.exe
  lecture.mp4        ->  Videos/lecture.mp4
  data.csv           ->  Spreadsheets/data.csv
  unknown_file.xyz   ->  Others/unknown_file.xyz

Done. 6 file(s) organized, 1 skipped.
```

---

## Customising it

To add your own category, just edit the `CATEGORIES` dictionary at the top of
the script:

```python
CATEGORIES = {
    "Ebooks": [".epub", ".mobi", ".azw3"],
    # ...existing categories...
}
```

---

## What I learned

- Working with paths using `pathlib` instead of string concatenation, so the
  script runs on both Windows and Linux
- The difference between `os.rename` and `shutil.move`, and why `shutil.move`
  is safer across drives
- Handling filename collisions instead of silently overwriting a user's files
- Adding a `--dry-run` flag &mdash; a habit taken from real infrastructure tools,
  where you always preview a destructive action before running it
- Reading command line arguments with `sys.argv`

---

## Possible improvements

- Sort by date (`2026-08/`) instead of by file type
- Add an undo option that reverses the last run
- Watch the folder continuously and organize new files automatically
- Add a simple GUI so non-technical users can run it
