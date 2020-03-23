
class FtBaseProject:
    def __init__(self, settings):
        self.settings = settings


    def create_new_project(self):
        print("Creating new project: " + self.settings["name"])
