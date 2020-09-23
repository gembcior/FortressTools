import os
import yaml

class ConfigParser:
    def get_config(config, project_type):
        config = os.path.abspath(os.path.expanduser(config))
        if not os.path.exists(config):
            raise Exception()
        settings = yaml.load(open(config, 'r'), Loader=yaml.FullLoader)
        if settings[project_type] is not None:
            return {**settings["general"], **settings[project_type]}
        else:
            return {**settings["general"]}
