#!/usr/bin/env python3

from fortresstools.menu.menu import FtMenu
from app.ftproject import run as FtProject
import os

def main():
    menu = FtMenu()
    menu.add_item("Projects", FtProject)
    menu.show()


if __name__ == "__main__":
    main()
