from .base_project import FtBaseProject

class FtQtProject(FtBaseProject):
    def __init__(self, settings):
        super(FtQtProject, self).__init__(settings)

    def create_new_project(self):
        print("Creating new Qt project: " + self.settings["name"])
