from .base_project import FtBaseProject


class FtCppProject(FtBaseProject):
    def __init__(self, settings, verbose=False):
        super(FtCppProject, self).__init__(settings, verbose)
