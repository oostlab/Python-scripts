#!/usr/bin/python3

# Program updating directories
# Author: Bert Oostland
# Version: 0.1
# date: 17-07-205
#
# usage: 
# Normal run (copies files)
# python sync_dirs.py --source /path/to/source --target /path/to/destination

# Dry run (no changes made)
# python sync_dirs.py -s /path/to/source -t /path/to/destination --dry-run

# Verbose output
# python sync_dirs.py -s /src -t /dst -v

import os
import shutil
import filecmp
import argparse
import shutil
import filecmp
import argparse

def sync_directories(source_dir, target_dir, dry_run=False, verbose=False):
    """
    Recursively compares source_dir to target_dir.
    Copies new or updated files from source_dir to target_dir.
    """
    # Ensure target_dir exists
    if not os.path.exists(target_dir):
        if verbose:
            print(f"Creating directory: {target_dir}")
        if not dry_run:
            os.makedirs(target_dir)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)

        if os.path.isfile(source_path):
            # Check if file is missing or different
            if not os.path.exists(target_path) or not filecmp.cmp(source_path, target_path, shallow=False):
                print(f"{'[DRY RUN] ' if dry_run else ''}Copying: {source_path} -> {target_path}")
                if not dry_run:
                    shutil.copy2(source_path, target_path)

        elif os.path.isdir(source_path):
            sync_directories(source_path, target_path, dry_run, verbose)

def main():
    parser = argparse.ArgumentParser(description="Recursively copy new or updated files from source to target directory.")
    parser.add_argument("--source", "-s", required=True, help="Path to source directory")
    parser.add_argument("--target", "-t", required=True, help="Path to target directory")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Show what would be copied without making changes")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed output")

    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f"Source directory does not exist: {args.source}")
        return

    sync_directories(args.source, args.target, dry_run=args.dry_run, verbose=args.verbose)

if __name__ == "__main__":
    main()
