import shutil
import unittest
import os
import subprocess


class BackportToolTestCase(unittest.TestCase):
    def setUp(self):
        # Set up any necessary configurations or variables
        self.tool_path = 'python backporter/app.py'  # Update with your tool path

    def test_backport_validation_files(self):
        validation_dir = 'testutils'
        validation_cases = os.listdir(validation_dir)

        for case in validation_cases:
            case_dir = os.path.join(validation_dir, case)
            before_file = os.path.join(case_dir, 'before_file_hash',
                                       os.listdir(os.path.join(case_dir, 'before_file_hash'))[0])
            after_file = os.path.join(case_dir, 'after_file_hash',
                                      os.listdir(os.path.join(case_dir, 'after_file_hash'))[0])
            target_file = os.path.join(case_dir, 'target_file_hash',
                                       os.listdir(os.path.join(case_dir, 'target_file_hash'))[0])

            # Create a copy of the target file for each test case
            target_copy = os.path.join(case_dir, 'target_copy.c')
            shutil.copyfile(target_file, target_copy)

            # Run the tool against the validation files
            try:
                subprocess.run(f'{self.tool_path} {before_file} {after_file} {target_copy}', shell=True, check=True)
            except subprocess.CalledProcessError as e:
                self.fail(f'Failed to run tool for validation case {case}. Error: {e}')


if __name__ == '__main__':
    unittest.main()
