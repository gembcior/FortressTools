from modules.runner.project.base_project_runner import BaseProjectRunner
from modules.settings.project.python_settings import FtPythonSettings
from modules.project.python_project import FtPythonProject

class PythonProjectRunner(BaseProjectRunner):
    def __init__(self):
        super(PythonProjectRunner, self).__init__()
        self._settings_object = FtPythonSettings()
        self._project_object = FtPythonProject

    @property
    def settings(self):
        self._settings["project_type"] = "python"
        self._settings = super().settings
        self._settings["project_template"] = "hello_world.yaml"
        return self._settings
