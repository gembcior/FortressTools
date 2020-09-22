from modules.runner.base_runner import BaseRunner

class CppRunner(BaseRunner):
    def __init__(self):
        super(BaseRunner, self).__init__()

    @property
    def settings(self):
        self._settings = super().settings
        return self._settings
