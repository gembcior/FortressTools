#!/usr/bin/env python3

from fortresstools.runner.project.stm32_project_runner import Stm32ProjectRunner
from fortresstools.runner.project.cpp_project_runner import CppProjectRunner
from fortresstools.runner.project.qt_project_runner import QtProjectRunner
from fortresstools.runner.project.python_project_runner import PythonProjectRunner
import argparse
import curses
import time

CMD_NONE = 0
CMD_NEW_PROJECT = 1
CMD_GUI = 2

SUPPORTED_PROJECTS = {"stm32": Stm32ProjectRunner(),
                      "cpp": CppProjectRunner(),
                      "python": PythonProjectRunner(),
                      "qt": QtProjectRunner()}


def run(projec_type="cpp"):
    SUPPORTED_PROJECTS[project_type].new_project()


def main():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument("-n", "--new",
                        action="store_const", dest="command", const=CMD_NEW_PROJECT, required=False,
                        help='Create new project')
    parser.add_argument("-t" "--type",
                        action="store", dest="project_type", required=False,
                        help="Type of project to work on")
    parser.add_argument("-v", "--verbose",
                        action="store_true", dest="verbose", required=False,
                        help='Increase logs verbosity level')
    args = parser.parse_args()

    if args.command == CMD_NEW_PROJECT and args.project_type is not None:
        SUPPORTED_PROJECTS[args.project_type].new_project()


if __name__ == "__main__":
    main()
