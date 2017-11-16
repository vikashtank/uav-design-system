"""
class to wrap the Popen class from the subprocess library
"""
import subprocess
import os
import shutil


class Runner():

    def __init__(self, file_path):
        # make a temp folder to run analysis in
        self.temp_folder = os.path.join(os.path.dirname(__file__), "run_time")
        # copy the executable to the temp file
        shutil.copy(file_path, self.temp_folder)
        # create a variable for the path to the new location of the executable
        self.executable = os.path.join(self.temp_folder, file_path)


    def _move_to_runtime(self, run_time_path, file_path):

        shutil.copy(file_path, run_time_path)

        return os.path.join(run_time_path, os.path.basename(file_path))


class Process():

    def __init__(self, process):
        self.process = process

    def command(self, command):
        command = self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        return command

    @staticmethod
    def initialise_process(file_path):

        process = subprocess.Popen([file_path], stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        universal_newlines=True)

        return Process(process)

    def print_it(self):
        self.process.stdin.close()
        i = 0
        while i < 500:
            i += 1
            print(self.process.stdout.readline())
