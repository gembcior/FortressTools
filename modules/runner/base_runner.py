from modules.parser.config.config_parser import ConfigParser
import importlib.resources as resources

class BaseRunner:
    def __init__(self):
        self._settings = None
        self._settings_object = None
        self._project_object = None

    @property
    def settings(self):
        self._settings = {}
        #settings["name"] = input("Project name: ")
        #settings["type"] = input("Project type: ")
        self._settings["name"] = "TestProject"
        self._settings["project_type"] = "cpp"
        with resources.path('config', 'default.cfg') as config:
            self._settings.update(ConfigParser.get_config(config, self._settings["project_type"]))
        return self._settings

    def new_project(self):
        print("new_project")
        settings = self.settings
        for item in settings:
            setattr(self._settings_object, item, settings[item])
        ft_project = self._project_object(self._settings_object)
        ft_project.make()
