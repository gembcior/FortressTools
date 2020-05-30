import logging
import os
from ..parser.project.project_template_parser import ProjectTemplateParser
from ..logger.logger import FtLogger


class FtBaseProject:
    def __init__(self, settings, verbose=False):
        self.settings = settings
        self.verbose = verbose
        self._start_logging(self.__class__.__name__)

    def _start_logging(self, name):
        if self.verbose is True:
            log_verbose = "DEBUG"
        else:
            log_verbose = "INFO"
        self.log = FtLogger.get_logger(name, log_verbose)

    def _create_directories(self, directories):
        for directory in directories:
            path = os.path.join(self.settings.project_directory, directory)
            os.makedirs(path, exist_ok=True)

    def _create_files(self, files):
        project_params_parser = ProjectTemplateParser(self.project_template_file)
        for file in files:
            if files[file] != "None":
                template_file = os.path.join(self.settings.templates, "ftt", self.settings.project_type, files[file])
                if not os.path.exists(template_file):
                    self.log.warning("Missing template file: " + template_file)
                    continue
                else:
                    with open(template_file, 'r') as template:
                        for line in template.readlines():
                            output_file = os.path.join(self.settings.workspace, self.settings.name, file)
                            with open(output_file, 'a') as output_file_temp:
                                output_file_temp.write(project_params_parser.get_line(line, self.settings))

    def _create_config_file(self):
        project_config_file = os.path.join(self.settings.project_directory, "project.ft")
        with open(project_config_file, "a") as file:
            settings = vars(self.settings)
            for setting in settings:
                file.write("%s: %s\n" % (setting, settings[setting]))

    def _setup_phase(self):
        self.log.debug("_setup_phase".upper())

    def _pre_project_structure_phase(self):
        self.log.debug("_pre_project_structure_phase".upper())

    def _project_structure_phase(self):
        self.log.debug("_project_structure_phase".upper())
        try:
            os.mkdir(self.settings.project_directory)
        except FileExistsError:
            raise Exception("Project %s already exists!" % self.settings.project_directory)
        project_template_parser = ProjectTemplateParser(self.project_template_file)
        directories, files = project_template_parser.get_project_items()
        self._create_directories(directories)
        self._create_files(files)

    def _post_project_structure_phase(self):
        self.log.debug("_post_project_structure".upper())

    def _pre_main_phase(self):
        self.log.debug("_pre_main_phase".upper())

    def _main_phase(self):
        self.log.debug("_main_phase".upper())

    def _post_main_phase(self):
        self.log.debug("_post_main_phase".upper())

    def _report_phase(self):
        self.log.debug("_report_phase".upper())

    def _final_phase(self):
        self.log.debug("_final_phase".upper())
        self._create_config_file()

    def make(self):
        self._setup_phase()
        self._pre_project_structure_phase()
        self._project_structure_phase()
        self._post_project_structure_phase()
        self._pre_main_phase()
        self._main_phase()
        self._post_main_phase()
        self._report_phase()
        self._final_phase()
