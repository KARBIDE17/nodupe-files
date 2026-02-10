# No Duplicates Files

This script scans a folder and removes duplicate files based on normalized filenames.

It treats these as the same base name:
- name.txt
- name_1.txt
- name 2.txt
- name (1).txt
- name copy.txt

Only one file per normalized name and extension is kept.

## Requirements

- Python 3.8+ (any recent Python 3 should work)

## How to run (start to finish)

1. Open a terminal in the project folder.

2. (RECOMMENDED) Do a dry run to see what would be deleted:

   ```bash
   python3 nodupe_files.py /path/to/folder --dry-run
   ```

3. Run for real to delete duplicates:

   ```bash
   python3 nodupe_files.py /path/to/folder
   ```

## Notes

- The script scans subfolders recursively.
- Duplicates are grouped by normalized name + file extension.
- The first file encountered is kept; the rest are removed.

## Example

```bash
python update.py ~/Downloads --dry-run
```
