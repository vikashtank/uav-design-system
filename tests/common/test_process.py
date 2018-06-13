from os.path import join, exists, dirname, abspath
from os import makedirs, getenv
from pathlib import Path
import sys
import unittest
import shutil

this_directory = Path(dirname(abspath(__file__)))
sys.path.append(str(this_directory) + '/../../')  # so uggo thanks to atom runner
from uav_design_system.common import Runner

class CustomFileAssertions():

    def read_file(self, file):
        with open(str(file)) as open_file:
            return open_file.read()

    def assertFilesSame(self, file1, file2):
        """
        tests that the content of two files are the same
        """
        file1_content = self.read_file(file1)
        file2_content = self.read_file(file2)

        if file1_content != file2_content:
            raise AssertionError('{0} is not the same as {1}'.format(file1,
                                                                     file2))
    def assertPathExists(self, path_object):
        self.assertTrue(path_object.exists())

    def assertPathNotExists(self, path_object):
        self.assertFalse(path_object.exists())


class TestRunner(unittest.TestCase, CustomFileAssertions):

    def setUp(self):
        self.temp_folder = Path(getenv('HOME')) / 'temp'

    def tearDown(self):
        pass

    def test_temp_file_created(self):
        runner = Runner('test file')
        self.assertPathExists(self.temp_folder)

    def test_runtimedir_property(self):
        runner = Runner('test file')
        self.assertEqual(str(self.temp_folder), runner.run_time_directory)

    def test_temp_file_replaced(self):
        self.temp_folder.mkdir()
        try:
            runner = Runner('test file')
        except FileExistsError:
            self.fail('file not replaced')

        self.assertPathExists(self.temp_folder)

    def test_move_to_runtime(self):
        runner = Runner('test_file')

    def test_delete(self):
        runner = Runner('test_file')
        del runner
        self.assertPathNotExists(self.temp_folder)


if __name__ == '__main__':
    unittest.main()
