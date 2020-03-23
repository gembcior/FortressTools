from .base_project import FtBaseProject


class FtCppProject(FtBaseProject):
    def __init__(self, settings):
        super(FtCppProject, self).__init__(settings)

    def create_new_project(self):
        print("Creating new Cpp project: " + self.settings["name"])
