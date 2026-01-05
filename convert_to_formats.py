#!/usr/bin/env python3
"""
Convert Research Application markdown files to PDF, HTML, and Word formats.

This script:
1. Takes all RA markdown files (RA01_*.md through RA10_*.md)
2. Converts them to PDF, HTML, and DOCX using pandoc
3. Organizes output into separate folders: pdf/, html/, word/

Requirements:
- pandoc must be installed (brew install pandoc on macOS)
- Python 3.6+
"""

import os
import subprocess
import sys
from pathlib import Path


def check_pandoc():
    """Check if pandoc is installed."""
    try:
        result = subprocess.run(['pandoc', '--version'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ pandoc is installed")
            return True
    except FileNotFoundError:
        return False


def create_directories(base_dir):
    """Create output directories if they don't exist."""
    dirs = {
        'pdf': base_dir / 'pdf',
        'html': base_dir / 'html',
        'word': base_dir / 'word',
    }

    for dir_name, dir_path in dirs.items():
        dir_path.mkdir(exist_ok=True)
        print(f"✓ Directory ready: {dir_path}")

    return dirs


def get_ra_files(base_dir):
    """Get all RA markdown files (RA01 through RA10)."""
    ra_files = []
    for i in range(1, 11):
        pattern = f"RA{i:02d}_*.md"
        matches = list(base_dir.glob(pattern))
        ra_files.extend(matches)

    ra_files.sort()
    return ra_files


def convert_file(input_file, output_dir, format_ext, format_type):
    """
    Convert a single markdown file to the specified format.

    Args:
        input_file: Path to input markdown file
        output_dir: Path to output directory
        format_ext: File extension (pdf, html, docx)
        format_type: Pandoc format specification (pdf, html5, docx)

    Returns:
        True if successful, False otherwise
    """
    output_filename = input_file.stem + '.' + format_ext
    output_file = output_dir / output_filename

    try:
        cmd = [
            'pandoc',
            str(input_file),
            '-f', 'markdown',
            '-t', format_type,
            '-o', str(output_file),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"  ✓ {format_ext.upper()}: {output_filename}")
            return True
        else:
            print(f"  ✗ {format_ext.upper()}: {output_filename}")
            print(f"    Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ {format_ext.upper()}: Error converting {input_file.name}")
        print(f"    {str(e)}")
        return False


def main():
    """Main conversion function."""
    # Set base directory
    base_dir = Path(__file__).parent.resolve()

    print("=" * 60)
    print("Research Applications Format Converter")
    print("=" * 60)
    print(f"Working directory: {base_dir}\n")

    # Check pandoc installation
    if not check_pandoc():
        print("\n✗ pandoc is not installed!")
        print("Install it with: brew install pandoc")
        sys.exit(1)

    print()

    # Create output directories
    print("Creating output directories...")
    dirs = create_directories(base_dir)
    print()

    # Get all RA markdown files
    ra_files = get_ra_files(base_dir)

    if not ra_files:
        print("✗ No RA markdown files found (looking for RA01_*.md through RA10_*.md)")
        sys.exit(1)

    print(f"Found {len(ra_files)} research applications to convert:\n")

    # Track conversion results
    total_conversions = 0
    successful_conversions = 0

    # Convert each file to each format
    for input_file in ra_files:
        print(f"Converting: {input_file.name}")

        # Convert to PDF
        if convert_file(input_file, dirs['pdf'], 'pdf', 'pdf'):
            successful_conversions += 1
        total_conversions += 1

        # Convert to HTML
        if convert_file(input_file, dirs['html'], 'html', 'html5'):
            successful_conversions += 1
        total_conversions += 1

        # Convert to DOCX
        if convert_file(input_file, dirs['word'], 'docx', 'docx'):
            successful_conversions += 1
        total_conversions += 1

        print()

    # Summary
    print("=" * 60)
    print("Conversion Summary")
    print("=" * 60)
    print(f"Total conversions attempted: {total_conversions}")
    print(f"Successful conversions: {successful_conversions}")
    print(f"Failed conversions: {total_conversions - successful_conversions}")
    print()

    if successful_conversions == total_conversions:
        print("✓ All conversions completed successfully!")
    else:
        print(f"⚠ {total_conversions - successful_conversions} conversion(s) failed.")

    print()
    print("Output structure:")
    print("  pdf/   - PDF versions of all RAs")
    print("  html/  - HTML versions of all RAs")
    print("  word/  - Word (.docx) versions of all RAs")
    print()


if __name__ == '__main__':
    main()
