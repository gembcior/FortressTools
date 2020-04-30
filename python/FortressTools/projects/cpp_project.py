from .base_project import FtBaseProject


class FtCppProject(FtBaseProject):
    def __init__(self, settings):
        super(FtCppProject, self).__init__(settings)
        self.settings["type"] = "cpp"
        self.settings["project_template"] = "empty.yaml"
