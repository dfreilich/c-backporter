import shutil
import unittest
import os
import subprocess

from backporter import app


class BackportToolTestCase(unittest.TestCase):
    def test_backport_validation_files(self):
        validation_dir = "testutils"
        validation_cases = os.listdir(validation_dir)

        for case in validation_cases:
            case_dir = os.path.join(validation_dir, case)
            before_file = os.path.join(
                case_dir,
                "before_file_hash",
                os.listdir(os.path.join(case_dir, "before_file_hash"))[0],
            )
            after_file = os.path.join(
                case_dir,
                "after_file_hash",
                os.listdir(os.path.join(case_dir, "after_file_hash"))[0],
            )
            target_file = os.path.join(
                case_dir,
                "target_file_hash",
                os.listdir(os.path.join(case_dir, "target_file_hash"))[0],
            )

            # Create a copy of the target file for each test case
            target_copy = os.path.join(case_dir, "target_copy.c")
            shutil.copyfile(target_file, target_copy)

            # Run the tool against the validation files
            try:
                app.run(before_file, after_file, target_copy)
            except subprocess.CalledProcessError as e:
                self.fail(f"Failed to run tool for case {case}. Error: {e}")


if __name__ == "__main__":
    unittest.main()
