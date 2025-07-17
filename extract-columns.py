#!/usr/bin/python3

# Program for cutting columns out of csv files
# Author: Bert Oostland
# Version: 0.1
# date: 17-07-205
#
# usage: python extract_columns.py data.csv 1 2 --sort 2 --no-header --output sorted.csv
import csv
import argparse
import sys

def try_numeric(val):
    """Try to convert a value to float if possible, else return a normalized string."""
    try:
        return float(val)
    except ValueError:
        return val.lower().strip()

# Argument parser
parser = argparse.ArgumentParser(description='Extract and optionally sort selected columns from a CSV file.')
parser.add_argument('input_file', help='Path to the input CSV file')
parser.add_argument('columns', type=int, nargs='+', help='Column numbers to extract (starting from 1)')
parser.add_argument('--output', '-o', default='selected_columns.txt',
                    help='Output file name (default: selected_columns.txt)')
parser.add_argument('--sort', type=int, help='Original column number (1-based) to sort the entire CSV by')
parser.add_argument('--no-header', action='store_true',
                    help='Specify if the input file has no header row')

args = parser.parse_args()

# Convert to zero-based indexes
column_indexes = [c - 1 for c in args.columns]
if any(c < 0 for c in column_indexes):
    print("❌ Error: Column numbers must be 1 or greater.")
    sys.exit(1)

sort_column_index = args.sort - 1 if args.sort else None
if sort_column_index is not None and sort_column_index < 0:
    print("❌ Error: Sort column must be 1 or greater.")
    sys.exit(1)

try:
    with open(args.input_file, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)

        # Read the first non-blank row
        first_row = None
        for row in reader:
            if any(cell.strip() for cell in row):
                first_row = row
                break
        else:
            print("❌ Error: Input CSV file is empty or has only blank lines.")
            sys.exit(1)

        rows = []
        if args.no_header:
            # No header: first row is data
            rows.append(first_row)
            num_columns = len(first_row)
        else:
            # Header present
            header = first_row
            num_columns = len(header)

        # Validate columns
        for i in column_indexes:
            if i >= num_columns:
                print(f"❌ Error: Column {i + 1} does not exist (only {num_columns} columns).")
                sys.exit(1)
        if sort_column_index is not None and sort_column_index >= num_columns:
            print(f"❌ Error: Sort column {args.sort} does not exist (only {num_columns} columns).")
            sys.exit(1)

        # Read remaining rows (skip blanks)
        for row in reader:
            if any(cell.strip() for cell in row):
                rows.append(row)

        # Normalize row lengths
        for row in rows:
            while len(row) < num_columns:
                row.append('')

        # Sort if needed
        if sort_column_index is not None:
            rows.sort(key=lambda r: try_numeric(r[sort_column_index]))

        # Write output
        with open(args.output, 'w', encoding='utf-8', newline='') as out_file:
            writer = csv.writer(out_file)

            if not args.no_header:
                writer.writerow([header[i] for i in column_indexes])

            for row in rows:
                writer.writerow([row[i] for i in column_indexes])

    print(f"✅ Output written to '{args.output}'"
          + (f", sorted by column {args.sort}" if args.sort else "")
          + (" (no header mode)" if args.no_header else ""))

except FileNotFoundError:
    print(f"❌ Error: File '{args.input_file}' not found.")
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
