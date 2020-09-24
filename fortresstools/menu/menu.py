import curses

class FtMenu:
    def __init__(self):
        pass

    def show(self):
        curses.wrapper(self._main_menu)

    def add_item(self, name, action):
        pass

    def _main_menu(self, stdscr):
        curses.curs_set(0)
        stdscr.clear()
        while True:
            stdscr.addstr(5, 5, "Main Menu")
            stdscr.refresh()
