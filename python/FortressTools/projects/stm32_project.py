import os
from .base_project import FtBaseProject
from ..utils.stm32_utils import FtStm32Utils


class FtStm32Project(FtBaseProject):
    def __init__(self, settings):
        super(FtStm32Project, self).__init__(settings)
        self.chip = FtStm32Utils.parse_chip_name(self.settings.chip)
        self.settings.cube = os.path.join(self.settings.cube, "STM32Cube" + self.chip["type"].upper() + self.chip["core"].upper())

    def _main_phase(self):
        super()._main_phase()
        utils = FtStm32Utils(self.settings)
        utils.update_cubemx_in_project(first_time=True)
