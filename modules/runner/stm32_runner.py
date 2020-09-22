from modules.runner.base_runner import BaseRunner
from modules.settings.stm32_settings import FtStm32Settings
from modules.projects.stm32_project import FtStm32Project

class Stm32Runner(BaseRunner):
    def __init__(self):
        super(BaseRunner, self).__init__()
        self._settings_object = FtStm32Settings()
        self._project_object = FtStm32Project

    @property
    def settings(self):
        self._settings = super().settings
        self._settings["chip"] = "stm32l152re"
        #self._settings["cubemx_project"] = "~/tools/STM32/Projects/STM32CMakeBlink/STM32CMakeBlink.ioc"
        self._settings["project_template"] = "stm32_blink_project_template.yaml"
        return self._settings
