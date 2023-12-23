#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys


def generate_patch(before_file, after_file):
    try:
        # Generate a patch file using diff command
        diff_process = subprocess.Popen(['diff', '-u', before_file, after_file], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        diff_output, _ = diff_process.communicate()

        # Check if diff succeeded (exit status 0 or 1 for differences found)
        if diff_process.returncode not in (0, 1):
            sys.exit(f"Error: Diff command failed with exit code {diff_process.returncode}")

        with open('patch.diff', 'wb') as patch_file:
            patch_file.write(diff_output)
    except Exception as e:
        print(f"Error during patch generation: {e}")
        sys.exit(1)


def apply_patch(target_file):
    try:
        # Apply patch to the target file
        patch_process = subprocess.Popen(['patch', target_file, 'patch.diff'], stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
        patch_output, _ = patch_process.communicate()

        if patch_process.returncode == 1:  # Indicates merge conflicts
            print("Merge conflicts detected. Check patch_log.txt for details.")
        elif patch_process.returncode != 0:
            sys.exit(f"Error: Patch failed with exit code {patch_process.returncode}")

        # Capture conflicts or success logs
        with open('patch_log.txt', 'wb') as log_file:
            log_file.write(patch_output)
    except Exception as e:
        print(f"Error during patch application: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 4:
        print("Usage: python run.py before.c after.c target.c")
        sys.exit(1)

    before_file, after_file, target_file = sys.argv[1], sys.argv[2], sys.argv[3]

    print("Generating patch")
    # Generate patch from before and after files
    generate_patch(before_file, after_file)

    print("Finished generating patches, starting to apply to target")
    # Apply patch to the target file
    apply_patch(target_file)
    print("Finished applying patches to target")


if __name__ == "__main__":
    main()
