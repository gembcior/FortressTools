from .base_project import FtBaseProject

class FtQtProject(FtBaseProject):
    def __init__(self, settings, verbose=False):
        super(FtQtProject, self).__init__(settings, verbose)

    def create_new_project(self):
        print("Creating new Qt project: " + self.settings["name"])
