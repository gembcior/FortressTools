from .base_project_runner import BaseProjectRunner

class QtProjectRunner(BaseProjectRunner):
    def __init__(self):
        super(QtProjectRunner, self).__init__()

    @property
    def settings(self):
        self._settings["project_type"] = "qt"
        self._settings = super().settings
        return self._settings
