import argparse
from xml.dom import minidom
import xml.etree.ElementTree as ET


class FtProject:
    def __init__(self, name):
        self.settings = {}
        self.settings["name"] = name

    def create_new_project(self):
        print("Creating new project: " + self.settings["name"])


def main():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument("-n", "--new",
                        action="store", dest="new_project", default=argparse.SUPPRESS, required=False,
                        help='Create new project')
    args = parser.parse_args()

    if "new_project" in args:
        ft_project = FtProject(name=args.new_project)
        ft_project.create_new_project()


if __name__ == "__main__":
    main()
