from .base_project_runner import BaseProjectRunner

class QtProjectRunner(BaseProjectRunner):
    def __init__(self):
        super(QtProjectRunner, self).__init__()
        self._settings["project_type"] = "qt"
