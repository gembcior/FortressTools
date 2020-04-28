from .base_project import FtBaseProject
import os
import tempfile
import subprocess
import re
from shutil import copyfile
from ..parser.project.project_template_parser import ProjectTemplateParser


class FtSTM32Project(FtBaseProject):
    def __init__(self, settings):
        super(FtSTM32Project, self).__init__(settings)
        must_args = ["stm32cubemx", "stm32cubemx_project", "stm32cube", "toolchain"
                     "stm32_chip", "stm32_family", "stm32_chip_type"]
#        if not all(arg in self.settings for arg in must_args):
#            raise Exception("Missing required settings for " + self.__class__.__name__)
        self.settings["type"] = "stm32"
        self.settings["project_template"] = "stm32_project_template.yaml"

    def _generate_cubemx_code(self):
        cubemx_dir = os.path.join(self.project_directory, "cubemx")
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
#        subprocess.run(cmd, shell=True, check=True)
        cubemx_script_file.close()

    def _copy_linker_script(self):
        path_pattern = re.compile(".*Projects/.*/Templates/SW4STM32.*")
        linker_script_pattern = ".*Linker script for " + self.settings["stm32_chip"].upper()
        if self.settings["stm32_chip_type"] is "xe":
            linker_script_pattern += "RETx.*"
        else:
            linker_script_pattern += "RETx.*"
        linker_script_pattern = re.compile(linker_script_pattern)
        found = None
        for path, dirs, files in os.walk(self.settings["stm32cube"]):
            if found is None:
                if re.search(path_pattern, path) is not None:
                    for file in [s for s in files if ".ld" in s]:
                        if found is None:
                            with open(os.path.join(path, file), 'r') as f:
                                for line in f:
                                    if re.search(linker_script_pattern, line) is not None:
                                        found = f.name
                                        break
                        else: break
            else: break
        if found is None:
            raise Exception()
        else:
            linker_script_pattern = re.compile(".*linker_script.ld")
            for file in self.files:
                if re.search(linker_script_pattern, file):
                    copyfile(found, os.path.join(self.project_directory, file))
                    break

    def _copy_startup_file(self):
        path_pattern = re.compile(".*Drivers/CMSIS/Device/ST/.*/Source/Templates/gcc")
        startup_file_pattern = re.compile("startup_" + self.settings["stm32_chip"] + self.settings["stm32_chip_type"] + ".s")
        found = None
        for path, dirs, files in os.walk(self.settings["stm32cube"]):
            if found is None:
                if re.search(path_pattern, path) is not None:
                    for file in [s for s in files if ".s" in s]:
                        if found is None:
                            if re.search(startup_file_pattern, file) is not None:
                                found = os.path.join(path, file)
                                break
                        else: break
            else: break
        if found is None:
            raise Exception()
        else:
            startup_file_pattern = re.compile(".*startup.s")
            for file in self.files:
                if re.search(startup_file_pattern, file):
                    copyfile(found, os.path.join(self.project_directory, file))
                    break

    def _copy_cubemx_files(self):
        src_files = os.listdir(os.path.join(self.project_directory, "cubemx", "Src"))
        for file in src_files:
            if re.search(".*_it.c", file) is None:
                copyfile(os.path.join(self.project_directory, "cubemx", "Src", file),
                         os.path.join(self.project_directory, "source", "cubemx", "src", file))

        inc_files = os.listdir(os.path.join(self.project_directory, "cubemx", "Inc"))
        for file in inc_files:
            if re.search(".*_it.h", file) is None:
                copyfile(os.path.join(self.project_directory, "cubemx", "Inc", file),
                         os.path.join(self.project_directory, "source", "cubemx", "inc", "cubemx", file))

    def _make_irq_lib(self):
        pass

    def _make_main_app(self):
        pass

    def _pre_main_phase(self):
        super()._pre_main_phase()
        self._generate_cubemx_code()

    def _main_phase(self):
        super()._main_phase()
        self._copy_startup_file()
        self._copy_linker_script()
        self._copy_cubemx_files()
        self._make_irq_lib()
        self._make_main_app()

    def _post_main_phase(self):
        super()._post_main_phase()
