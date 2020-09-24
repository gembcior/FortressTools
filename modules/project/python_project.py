from .base_project import FtBaseProject


class FtPythonProject(FtBaseProject):
    def __init__(self, settings, verbose=False):
        super(FtPythonProject, self).__init__(settings, verbose)
