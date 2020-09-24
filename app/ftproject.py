#!/usr/bin/env python3

from modules.runner.project.stm32_project_runner import Stm32ProjectRunner
from modules.runner.project.cpp_project_runner import CppProjectRunner
from modules.runner.project.qt_project_runner import QtProjectRunner
import argparse
import curses
import time

CMD_NONE = 0
CMD_NEW_PROJECT = 1
CMD_GUI = 2

SUPPORTED_PROJECTS = {"stm32": Stm32ProjectRunner(),
                      "cpp": CppProjectRunner(),
                      "qt": QtProjectRunner()}

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
    parser.add_argument("-g", "--gui",
                        action="store_const", dest="command", const=CMD_GUI, required=False,
                        help='Start GUI')
    args = parser.parse_args()

    if args.command == CMD_NEW_PROJECT and args.project_type is not None:
        SUPPORTED_PROJECTS[args.project_type].new_project()


if __name__ == "__main__":
    main()
