from modules.runner.base_runner import BaseRunner
from modules.settings.cpp_settings import FtCppSettings
from modules.projects.cpp_project import FtCppProject

class CppRunner(BaseRunner):
    def __init__(self):
        super(CppRunner, self).__init__()
        self._settings_object = FtCppSettings()
        self._project_object = FtCppProject

    @property
    def settings(self):
        self._settings["project_type"] = "cpp"
        self._settings = super().settings
        self._settings["project_template"] = "hello_world.yaml"
        return self._settings
