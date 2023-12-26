#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import re
import shutil
import subprocess
import sys


def generate_patch(before_file, after_file):
    try:
        # Generate a patch file using diff command
        diff_process = subprocess.Popen(
            ["diff", "-u", before_file, after_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        diff_output, _ = diff_process.communicate()

        # Check if diff succeeded (exit status 0 or 1 for differences found)
        if diff_process.returncode not in (0, 1):
            sys.exit(
                f"Error: Diff command failed with exit code"
                f" {diff_process.returncode}"
            )

        with open("patch.diff", "wb") as patch_file:
            patch_file.write(diff_output)
    except Exception as e:
        print(f"Error during patch generation: {e}")
        sys.exit(1)


def write_patch_log(patch_output, log_path, target_file):
    # Extract conflicted hunks' start and end lines from the output
    conflict_lines = [
        line
        for line in patch_output.decode("utf-8").splitlines()
        if line.startswith("Hunk #")
    ]

    conflict_info = "\n".join(conflict_lines)
    failed_hunks_last_line = re.search(
        r"(\d+) out of (\d+) hunks", patch_output.decode("utf-8")
    )

    # Write conflict information to patch_log.txt
    with open(log_path, "a") as log_file:
        log_file.write(f"Patches for File {target_file}\n")
        log_file.write(conflict_info)
        if failed_hunks_last_line:
            total_failed, total_hunks = failed_hunks_last_line.groups()
            log_file.write(
                f"\nTotal failed hunks: {total_failed} " f"out of {total_hunks}\n"
            )


def apply_patch(target_file, output_dir=""):
    try:
        # Create a copy of the target file as result.c
        target_path = os.path.join(output_dir, "result.c")
        log_path = os.path.join(output_dir, "patch_log.txt")
        shutil.copyfile(target_file, target_path)

        # Apply patch to the target file
        patch_process = subprocess.Popen(
            ["patch", "--verbose", target_path, "-i", "patch.diff", "-f"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        patch_output, _ = patch_process.communicate()

        if patch_process.returncode not in (0, 1):
            code = patch_process.returncode
            sys.exit(f"Error: Patch failed with exit code {code}")

        print(f"Patch concluded, writing log file to {log_path}")
        write_patch_log(patch_output, log_path, target_path)

    except Exception as e:
        print(f"Error during patch application: {e}")
        sys.exit(1)


def run(before_file, after_file, target_file, output_dir=""):
    print("Generating patch")
    # Generate patch from before and after files
    generate_patch(before_file, after_file)

    print("Finished generating patches, starting to apply to target")
    # Apply patch to the target file
    apply_patch(target_file, output_dir)
    print("Finished applying patches to target")


def main():
    parser = argparse.ArgumentParser(description="Backporting Tool")
    parser.add_argument("before_file", help='Path to the "before" file')
    parser.add_argument("after_file", help='Path to the "after" file')
    parser.add_argument("target_file", help='Path to the "target" file')
    parser.add_argument(
        "--outputdir", "-o", help="Output directory (optional)", default=""
    )
    args = parser.parse_args()

    run(args.before_file, args.after_file, args.target_file, args.outputdir)


if __name__ == "__main__":
    main()
