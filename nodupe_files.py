import argparse
import os
import re
from pathlib import Path

COPY_REGEX = re.compile(r"[ _-]copy(\s*\(?\d+\)?)?$", re.IGNORECASE)
NUMBER_REGEX = re.compile(r"[ _-]?\(?\d+\)?$", re.IGNORECASE)


def normalize_stem(stem):
    normalized = stem.strip()
    while True:
        updated = COPY_REGEX.sub("", normalized).strip()
        updated = NUMBER_REGEX.sub("", updated).strip(" _-()")
        if updated == normalized:
            break
        normalized = updated
    return normalized


def dedupe_folder(folder_path, dry_run=False):
    kept = {}
    deleted = []
    skipped = []

    for root, _, files in os.walk(folder_path):
        for filename in files:
            path = Path(root) / filename
            if not path.is_file():
                continue

            stem = path.stem
            ext = path.suffix.lower()
            key = (normalize_stem(stem).lower(), ext)

            if key in kept:
                deleted.append(path)
                if not dry_run:
                    path.unlink()
            else:
                kept[key] = path
                skipped.append(path)

    return kept, deleted, skipped


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Remove duplicate files by normalizing filenames like: "
            "name, name_1, name 2, name (1), name copy"
        )
    )
    parser.add_argument("folder", help="Folder to scan recursively")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without removing files",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    target = Path(args.folder).expanduser().resolve()

    if not target.exists() or not target.is_dir():
        raise SystemExit("Folder does not exist or is not a directory.")

    kept, deleted, _ = dedupe_folder(target, dry_run=args.dry_run)

    print(f"Scanned: {target}")
    print(f"Kept:    {len(kept)}")
    print(f"Deleted: {len(deleted)}")
    if args.dry_run and deleted:
        print("\nWould delete:")
        for path in deleted:
            print(f"- {path}")