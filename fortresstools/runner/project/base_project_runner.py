from ...parser.config.config_parser import ConfigParser
import importlib.resources as resources
import os
import re
import yaml

class BaseProjectRunner:
    def __init__(self):
        self._settings = {}
        self._settings["project_type"] = "base"
        self._settings_object = None
        self._project_object = None

    def _find_project_config_file(self):
        dirs = os.getcwd().split("/")
        dirs_list = []
        for index in range(2, len(dirs) + 1):
            dirs_list.append(os.path.abspath("/".join(dirs[:index])))
        dirs_list.reverse()

        pattern = re.compile("project.ft")
        settings_file = None
        for directory in dirs_list:
            for file in [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]:
                if re.search(pattern, file):
                    settings_file = os.path.join(directory, file)
                    break
            if settings_file is not None:
                break
        project_config_file = settings_file
        return project_config_file

    def _get_settings_from_project_config_file(self, project_config_file):
        settings = yaml.load(open(project_config_file, 'r'), Loader=yaml.FullLoader)
        return settings

    def _get_settings_from_config_file(self, package=__name__.split(".")[0], config_file="default.cfg"):
        settings = {}
        with resources.path(package + '.config', config_file) as config:
            settings.update(ConfigParser.get_config(config, self._settings["project_type"]))
        return settings

    def _get_settings_from_input(self):
        settings = {}
        return settings

    @property
    def settings(self):
        project_config_file = self._find_project_config_file()
        if project_config_file is not None:
            self._settings.update(self._get_settings_from_project_config_file(project_config_file))
        else:
            self._settings["name"] = input("Project name: ")
            self._settings.update(self._get_settings_from_config_file())
            self._settings.update(self._get_settings_from_input())
        return self._settings

    def new_project(self):
        settings = self.settings
        for item in settings:
            setattr(self._settings_object, item, settings[item])
        ft_project = self._project_object(self._settings_object, True)
        ft_project.make()
