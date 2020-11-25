from .base_project_runner import BaseProjectRunner
from ...settings.project.python_settings import FtPythonSettings
from ...project.python_project import FtPythonProject

class PythonProjectRunner(BaseProjectRunner):
    def __init__(self):
        super(PythonProjectRunner, self).__init__()
        self._settings["project_type"] = "python"
        self._settings_object = FtPythonSettings()
        self._project_object = FtPythonProject

    def _get_settings_from_input(self):
        settings = {}
        settings["project_template"] = "hello_world.yaml"
        return settings
