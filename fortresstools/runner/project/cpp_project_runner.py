from .base_project_runner import BaseProjectRunner
from ...settings.project.cpp_settings import FtCppSettings
from ...project.cpp_project import FtCppProject

class CppProjectRunner(BaseProjectRunner):
    def __init__(self):
        super(CppProjectRunner, self).__init__()
        self._settings["project_type"] = "cpp"
        self._settings_object = FtCppSettings()
        self._project_object = FtCppProject

    def _get_settings_from_input(self):
        settings = {}
        settings["project_template"] = "hello_world.yaml"
        return settings
