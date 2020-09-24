from .base_settings import FtBaseSettings
import os


class FtStm32Settings(FtBaseSettings):
    def __init__(self):
        super(FtStm32Settings, self).__init__()
        self._cubemx = None
        self._cubemx_project = None
        self._cube = None
        self._toolchain = None
        self._chip = None

    @property
    def cubemx(self):
        return self._cubemx

    @cubemx.setter
    def cubemx(self, value):
        cubemx = os.path.expanduser(value)
        cubemx = os.path.abspath(cubemx)
        if os.path.exists(cubemx):
            self._cubemx = cubemx
        else:
            raise Exception("Unable to set cubemx property. Directory does not exist.")

    @property
    def cubemx_project(self):
        return self._cubemx_project

    @cubemx_project.setter
    def cubemx_project(self, value):
        cubemx_project = os.path.expanduser(value)
        cubemx_project = os.path.abspath(cubemx_project)
        if os.path.exists(cubemx_project):
            self._cubemx_project = cubemx_project
        else:
            raise Exception("Unable to set cubemx_project property. File does not exist.")

    @property
    def cube(self):
        return self._cube

    @cube.setter
    def cube(self, value):
        cube = os.path.expanduser(value)
        cube = os.path.abspath(cube)
        if os.path.exists(cube):
            self._cube = cube
        else:
            raise Exception("Unable to set cube property. Directory does not exist.")

    @property
    def toolchain(self):
        return self._toolchain

    @toolchain.setter
    def toolchain(self, value):
        toolchain = os.path.expanduser(value)
        toolchain = os.path.abspath(toolchain)
        if os.path.exists(toolchain):
            self._toolchain = toolchain
        else:
            raise Exception("Unable to set toolchain property. Directory does not exist.")

    @property
    def chip(self):
        return self._chip

    @chip.setter
    def chip(self, value):
        self._chip = value.strip()

    @property
    def cubemx_origin_directory(self):
        self._cubemx__directory = os.path.join(self.project_directory, "cubemx")
        return self._cubemx__directory

    @property
    def cubemx_target_directory(self):
        self._cubemx__directory = os.path.join(self.project_directory, "source", "cubemx")
        return self._cubemx__directory
