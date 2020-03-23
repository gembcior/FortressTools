from .base_project import FtBaseProject
import os
from ..parser.ftt.ftt_parser import FttFileParser
from ..parser.project.project_template_parser import ProjectTemplateParser
from ..parser.params.params_parser import ParamsParser


class FtSTM32Project(FtBaseProject):
    def __init__(self, settings):
        super(FtSTM32Project, self).__init__(settings)

        self.settings["type"] = "STM32"
        self.settings["dir_struct"] = "stm32_project_dir_structure.yaml"

        self.project_template_parser = ProjectTemplateParser()
        self.ftt_file_parser = FttFileParser()
        self.params_parser = ParamsParser()

    def _parse_project_template(self):
        project_template_file = os.path.join(self.settings["templates"], "project/stm32_project_template.yaml")
        self.project_template_parser.run(project_template_file)


    def create_new_project(self):
        assert os.path.exists(self.settings["workspace"])

        print("Type:      " + self.settings["type"])
        print("Name:      " + self.settings["name"])
        print("Workspace: " + self.settings["workspace"])

        self._parse_project_template()
