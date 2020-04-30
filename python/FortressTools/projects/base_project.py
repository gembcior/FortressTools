import logging
import os
from ..parser.project.project_template_parser import ProjectTemplateParser


class FtBaseProject:
    def __init__(self, settings):
        self.settings = settings
        must_args = ["name", "workspace", "templates"]
        if not all(arg in self.settings for arg in must_args):
            raise Exception("Missing required settings for " + self.__class__.__name__)
        if "verbose" not in self.settings:
            self.settings["verbose"] = False
        self._start_logging(self.__class__.__name__)

    def _start_logging(self, name):
        if self.settings["verbose"] is True:
            log_verbose = logging.DEBUG
        else:
            log_verbose = logging.INFO
        self.log = logging.getLogger(name)
        self.log.setLevel(log_verbose)
        self.log_handler = logging.StreamHandler()
        self.log_handler.setLevel(log_verbose)
        self.log_formatter = logging.Formatter("[%(levelname)s][%(name)s] %(message)s")
        self.log_handler.setFormatter(self.log_formatter)
        self.log.addHandler(self.log_handler)

    def _create_directories(self, directories):
        for directory in directories:
            path = os.path.join(self.project_directory, directory)
            os.makedirs(path, exist_ok=True)

    def _create_files(self, files):
        project_params_parser = ProjectTemplateParser(self.project_template_file)
        for file in files:
            if files[file] != "None":
                template_file = os.path.join(self.settings["templates"], "ftt", self.settings["type"], files[file])
                if not os.path.exists(template_file):
                    self.log.warning("Missing template file: " + template_file)
                    continue
                else:
                    with open(template_file, 'r') as template:
                        for line in template.readlines():
                            output_file = os.path.join(self.settings["workspace"], self.settings["name"], file)
                            with open(output_file, 'a') as output_file_temp:
                                output_file_temp.write(project_params_parser.get_line(line))

    def _create_config_file(self):
        project_config_file = os.path.join(self.project_directory, "project.ft")
        with open(project_config_file, "a") as file:
            for setting in self.settings:
                file.write("%s: %s\n" % (setting, self.settings[setting]))

    def _setup_phase(self):
        self.log.debug("_setup_phase".upper())
        if not os.path.exists(self.settings["workspace"]):
            raise Exception()
        self.project_template_file = os.path.join(self.settings["templates"], "project", self.settings["project_template"])
        if not os.path.exists(self.project_template_file):
            raise Exception()
        self.project_directory = os.path.join(self.settings["workspace"], self.settings["name"])

    def _pre_project_structure_phase(self):
        self.log.debug("_pre_project_structure_phase".upper())

    def _project_structure_phase(self):
        self.log.debug("_project_structure_phase".upper())
        try:
            os.mkdir(self.project_directory)
        except FileExistsError:
            raise Exception("Project %s already exists!" % self.project_directory)
        project_template_parser = ProjectTemplateParser(self.project_template_file)
        directories, self.files = project_template_parser.get_project_items()
        self._create_directories(directories)
        self._create_files(self.files)

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
