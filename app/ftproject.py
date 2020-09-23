from modules.runner.stm32_runner import Stm32Runner
from modules.runner.cpp_runner import CppRunner
from modules.runner.qt_runner import QtRunner
import argparse

CMD_NONE = 0
CMD_NEW_PROJECT = 1

SUPPORTED_PROJECTS = {"stm32": Stm32Runner(),
                      "cpp": CppRunner(),
                      "qt": QtRunner()}

def main():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument("-n", "--new",
                        action="store_const", dest="command", const=CMD_NEW_PROJECT, required=False,
                        help='Create new project')
    parser.add_argument("-t" "--type",
                        action="store", dest="project_type", required=True,
                        help="Type of project to work on")
    parser.add_argument("-v", "--verbose",
                        action="store_true", dest="verbose", required=False,
                        help='Increase logs verbosity level')
    args = parser.parse_args()

    if args.command == CMD_NEW_PROJECT:
        SUPPORTED_PROJECTS[args.project_type].new_project()


if __name__ == "__main__":
    main()
