from modules.runner.base_runner import BaseRunner

class QtRunner(BaseRunner):
    def __init__(self):
        super(BaseRunner, self).__init__()

    @property
    def settings(self):
        self._settings["project_type"] = "qt"
        self._settings = super().settings
        return self._settings
