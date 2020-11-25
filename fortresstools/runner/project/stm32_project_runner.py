from .base_project_runner import BaseProjectRunner
from ...settings.project.stm32_settings import FtStm32Settings
from ...project.stm32_project import FtStm32Project

class Stm32ProjectRunner(BaseProjectRunner):
    def __init__(self):
        super(Stm32ProjectRunner, self).__init__()
        self._settings["project_type"] = "stm32"
        self._settings_object = FtStm32Settings()
        self._project_object = FtStm32Project

    def _get_settings_from_input(self):
        settings = {}
        settings["chip"] = input("Chip: ")
        settings["cubemx_project"] = input("CubeMX project: ")
        settings["project_template"] = "blink_project_template.yaml"
        return settings
