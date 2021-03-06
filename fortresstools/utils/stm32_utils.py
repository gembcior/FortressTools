from ..project.base_project import FtBaseProject
from ..parser.project.project_template_parser import ProjectTemplateParser
from ..logger.logger import FtLogger
import os
import tempfile
import subprocess
import re
from shutil import copyfile
import diff_match_patch as diff_tool
import importlib.resources as resources


class FtStm32Utils():
    def __init__(self, settings, verbose=False):
        self.settings = settings
        self.chip = FtStm32Utils.parse_chip_name(self.settings.chip)
        self.verbose = verbose
        self._start_logging(self.__class__.__name__)

    def _start_logging(self, name):
        if self.verbose is True:
            log_verbose = "DEBUG"
        else:
            log_verbose = "INFO"
        self.log = FtLogger.get_logger(name, log_verbose)

    def _get_linker_script(self):
        path_pattern = re.compile(".*Projects/.*/Templates/SW4STM32.*")
        linker_script_pattern = ".*Linker script for " + self.settings.chip.upper() + ".*"
        linker_script_pattern = re.compile(linker_script_pattern)
        found = None
        for path, dirs, files in os.walk(os.path.expanduser(self.settings.cube)):
            if found is None:
                if re.search(path_pattern, path) is not None:
                    for file in [s for s in files if ".ld" in s]:
                        if found is None:
                            encodings = ['utf-8', 'latin_1']
                            for e in encodings:
                                try:
                                    with open(os.path.join(path, file), 'r', encoding=e) as f:
                                        for line in f:
                                            if re.search(linker_script_pattern, line) is not None:
                                                found = f.name
                                                break
                                except UnicodeDecodeError:
                                    self.log.warning("Unicode Decode Error for %s with %s, trying different encoding" % (file, e))
                                else:
                                    break
                        else: break
            else: break
        if found is not None:
            return found
        else:
            raise Exception()

    def _find_startup_file(self, chip):
        path_pattern = re.compile(".*Drivers/CMSIS/Device/ST/.*/Source/Templates/gcc")
        startup_file_pattern = re.compile("startup_" + chip + ".s")
        found = None
        for path, dirs, files in os.walk(os.path.expanduser(self.settings.cube)):
            if found is None:
                if re.search(path_pattern, path) is not None:
                    for file in [s for s in files if ".s" in s]:
                        if found is None:
                            if re.search(startup_file_pattern, file) is not None:
                                found = os.path.join(path, file)
                                break
                        else: break
            else: break
        return found

    def _get_startup_file(self):
        chip_names = [self.chip["family"] + self.chip["type"] + self.chip["core"] + self.chip["line"] + "x" + "x",
                      self.chip["family"] + self.chip["type"] + self.chip["core"] + self.chip["line"] + "x" + self.chip["flash"],
                      self.chip["family"] + self.chip["type"] + self.chip["core"] + self.chip["line"] + self.chip["pins"] + "x"]
        for chip in chip_names:
            result = self._find_startup_file(chip)
            if result is not None:
                return result
        raise Exception("Unable to find startup file for chip: " + self.settings.chip)

    def _diff(self, file1, file2):
        dmp = diff_tool.diff_match_patch()
        diff = dmp.diff_main(file1, file2)
        patch = dmp.patch_make(file1, diff)
        file3, result = dmp.patch_apply(patch, file1)
        return file3

    def _copy_cubemx_files(self):
        project_directory = os.path.join(os.path.expanduser(self.settings.workspace), self.settings.name)
        if not os.path.exists(project_directory):
            raise Exception()
        src_dest_dir = os.path.join(project_directory, "source", "cubemx", "src")
        inc_dest_dir = os.path.join(project_directory, "source", "cubemx", "inc", "cubemx")
        src_source_dir = os.path.join(project_directory, "cubemx", "Src")
        inc_source_dir = os.path.join(project_directory, "cubemx", "Inc")

        if not os.listdir(src_dest_dir) and not os.listdir(inc_dest_dir):
            for file in os.listdir(src_source_dir):
                if re.search(".*_it.c", file) is None:
                    copyfile(os.path.join(src_source_dir, file),
                            os.path.join(src_dest_dir, file))

            for file in os.listdir(inc_source_dir):
                if re.search(".*_it.h", file) is None:
                    copyfile(os.path.join(inc_source_dir, file),
                            os.path.join(inc_dest_dir, file))

    def _update_cubemx_files_in_project(self):
        project_directory = os.path.join(self.settings.workspace, self.settings.name)
        if not os.path.exists(project_directory):
            raise Exception()
        src_dest_dir = os.path.join(project_directory, "source", "cubemx", "src")
        inc_dest_dir = os.path.join(project_directory, "source", "cubemx", "inc", "cubemx")
        src_source_dir = os.path.join(project_directory, "cubemx", "Src")
        inc_source_dir = os.path.join(project_directory, "cubemx", "Inc")

        for file in os.listdir(src_dest_dir):
            copyfile(os.path.join(src_dest_dir, file),
                        os.path.join(src_source_dir, file))

        for file in os.listdir(inc_dest_dir):
            copyfile(os.path.join(inc_dest_dir, file),
                        os.path.join(inc_source_dir, file))

        self.generate_cubemx_code(os.path.join(project_directory, "cubemx", "cubemx.ioc"), project_directory)

        for file in os.listdir(src_dest_dir):
            old_file = open(os.path.join(src_dest_dir, file), "r")
            new_file = open(os.path.join(src_source_dir, file), "r")
            update = self._diff(old_file.read(), new_file.read())
            old_file.close()
            new_file.close()
            new_file = open(os.path.join(src_dest_dir, file), "w")
            new_file.write(update)
            new_file.close()

        for file in os.listdir(inc_dest_dir):
            old_file = open(os.path.join(inc_dest_dir, file), "r")
            new_file = open(os.path.join(inc_source_dir, file), "r")
            update = self._diff(old_file.read(), new_file.read())
            old_file.close()
            new_file.close()
            new_file = open(os.path.join(inc_dest_dir, file), "w")
            new_file.write(update)
            new_file.close()

        self._copy_cubemx_files()

    def _replace_file_in_project(self, source, destination):
        if not os.path.exists(source):
            raise Exception()
        project_directory = os.path.join(os.path.expanduser(self.settings.workspace), self.settings.name)
        if not os.path.exists(project_directory):
            raise Exception()
        project_template_file = self.settings.project_template
        if not os.path.exists(project_template_file):
            raise Exception()
        project_template_parser = ProjectTemplateParser(project_template_file)
        directories, files = project_template_parser.get_project_items()
        pattern = re.compile(".*" + destination)
        for file in files:
            if re.search(pattern, file):
                copyfile(source, os.path.join(project_directory, file))
                break

    def _get_irq_list(self, irq_source_file):
        irq_pattern = re.compile("(?<=void )(.*?)(?=\(void\))", re.MULTILINE)
        with open(irq_source_file, 'r') as f:
            irq_list = re.findall(irq_pattern, f.read())
        return irq_list

    def _make_irq_header_file(self, irq_header_file, irq_list):
        with open(irq_header_file, 'r') as f:
            lines = f.readlines()
        start_pattern = re.compile("^extern.*")
        end_pattern = re.compile("^}")
        for line in lines:
            if re.search(start_pattern, line):
                start_index = lines.index(line) + 1
            if re.search(end_pattern, line):
                end_index = lines.index(line)
        lines = lines[:start_index] + lines[end_index:]
        for i, irq in enumerate(irq_list):
            irq_declaration = "  void %s(void) __attribute__ ((interrupt (\"IRQ\")));\n" % irq
            lines.insert(start_index + i, irq_declaration)
        with open(irq_header_file, 'w') as f:
            f.writelines(lines)

    def _make_irq_source_file(self, irq_origin_source_file, irq_source_file):
        old_irq_list = self._get_irq_list(irq_source_file)
        new_irq_list = self._get_irq_list(irq_origin_source_file)
        irq_list = list(set(new_irq_list) - set(old_irq_list))
        irq_pattern = re.compile("(?=void )(.*?)(?<=^[}])", re.MULTILINE | re.DOTALL)
        with open(irq_origin_source_file, 'r') as f:
            irq_definition_list = re.findall(irq_pattern, f.read())
        comment_pattern = re.compile("(?=\/\*)(.*?)(?<=\*\/)", re.MULTILINE)
        for i, irq in enumerate(irq_definition_list):
            for comment in re.findall(comment_pattern, irq):
                irq = irq.replace(comment, '')
            irq_definition_list[i] = irq
        for irq in irq_definition_list:
            irq_pattern = re.compile("(?<=void )(.*?)(?=\(void\))", re.MULTILINE)
            if re.search(irq_pattern, irq).group(0) in irq_list:
                with open(irq_source_file, 'a') as f:
                    string_to_write = "\n\n%s\n" % irq
                    f.write(string_to_write)

    def _make_irq_lib(self):
        origin_source_dir = os.path.join(self.settings.cubemx_origin_directory, "Src")
        irq_source_dir = os.path.join(self.settings.project_directory, "source", "irq", "src")
        irq_header_dir = os.path.join(self.settings.project_directory, "source", "irq", "inc", "irq")

        irq_file_pattern = re.compile(".*_it.c")
        for file in os.listdir(origin_source_dir):
            if re.search(irq_file_pattern, file):
                irq_origin_source_file = os.path.join(origin_source_dir, file)

        irq_file_pattern = re.compile("irq.cpp")
        for file in os.listdir(irq_source_dir):
            if re.search(irq_file_pattern, file):
                irq_source_file = os.path.join(irq_source_dir, file)

        irq_file_pattern = re.compile("irq.h")
        for file in os.listdir(irq_header_dir):
            if re.search(irq_file_pattern, file):
                irq_header_file = os.path.join(irq_header_dir, file)

        self._make_irq_header_file(irq_header_file, self._get_irq_list(irq_origin_source_file))
        self._make_irq_source_file(irq_origin_source_file, irq_source_file)

    def _make_main_app(self):
        pass

    def parse_chip_name(name):
        if len(name) < 11:
            raise Exception()
        chip = {}
        chip["family"] = name[:5]
        chip["type"] = name[5:6]
        chip["core"] = name[6:7]
        chip["line"] = name[7:9]
        chip["pins"] = name[9:10]
        chip["flash"] = name[10:11]
        return chip


# TODO refactor
    def generate_cubemx_code(self, project, destination):
        if not os.path.exists(project):
            raise Exception()
        if not os.path.exists(destination):
            raise Exception()
        cubemx_dir = os.path.join(destination, "cubemx")
        cubemx_script = ["config load " + project + "\n",
                         "project name cubemx\n",
                         "project couplefilesbyip 1\n",
                         "project path " + cubemx_dir + "\n",
                         "generate code " + cubemx_dir + "\n",
                         "config saveas " + os.path.join(cubemx_dir, "cubemx.ioc") + "\n",
                         "exit\n"]
        cubemx_script_file = tempfile.NamedTemporaryFile(mode='w+t')
        cubemx_script_file.writelines(cubemx_script)
        cubemx_script_file.seek(0)
        cmd = "java " + "-jar " + self.settings.cubemx + " -q " + cubemx_script_file.name
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
        cubemx_script_file.close()

    def update_cubemx_in_project(self, first_time=False):
        project_directory = os.path.join(os.path.expanduser(self.settings.workspace), self.settings.name)
        if not os.path.exists(project_directory):
            raise Exception()
        if first_time:
            self.generate_cubemx_code(self.settings.cubemx_project, project_directory)
            self._replace_file_in_project(self._get_linker_script(), "linker_script.ld")
            self._replace_file_in_project(self._get_startup_file(), "startup.s")
            self._copy_cubemx_files()
            self._make_irq_lib()
        else:
            self._update_cubemx_files_in_project()


