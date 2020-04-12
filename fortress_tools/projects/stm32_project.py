from .base_project import FtBaseProject
import os
import tempfile
import subprocess


class FtSTM32Project(FtBaseProject):
    def __init__(self, settings):
        super(FtSTM32Project, self).__init__(settings)
        must_args = ["stm32cubemx", "stm32cubemx_project", "stm32cube", "toolchain"
                     "stm32_chip", "stm32_family", "stm32_chip_type"]
#        if not all(arg in self.settings for arg in must_args):
#            raise Exception("Missing required settings for " + self.__class__.__name__)
        self.settings["type"] = "stm32"
        self.settings["project_template"] = "stm32_project_template.yaml"
        self.settings["project_params"] = "stm32.yaml"

    def _generate_cubemx_code(self):
        cubemx_dir = os.path.join(self.settings["workspace"], self.settings["name"], "cubemx")
        cubemx_script = ["config load " + self.settings["stm32cubemx_project"] + "\n",
                         "project name cubemx\n",
                         "project couplefilesbyip 1\n",
                         "project path " + cubemx_dir + "\n",
                         "generate code " + cubemx_dir + "\n",
                         "config saveas " + os.path.join(cubemx_dir, "cubemx.ioc") + "\n",
                         "exit\n"]
        cubemx_script_file = tempfile.NamedTemporaryFile(mode='w+t')
        cubemx_script_file.writelines(cubemx_script)
        cubemx_script_file.seek(0)
        cmd = "java " + "-jar " + self.settings["stm32cubemx"] + " -q " + cubemx_script_file.name
        subprocess.run(cmd, shell=True, check=True)
        cubemx_script_file.close()

    def _pre_main_phase(self):
        super()._pre_main_phase()
        self._generate_cubemx_code()

    def _main_phase(self):
        super()._main_phase()
        print(os.listdir(os.path.join(self.settings["workspace"], self.settings["name"], "cubemx", "Src")))
        print(os.listdir(os.path.join(self.settings["workspace"], self.settings["name"], "cubemx", "Inc")))

    def _post_main_phase(self):
        super()._post_main_phase()
