import argparse
import os
from FortressTools.projects.cpp_project import FtCppProject
from FortressTools.projects.stm32_project import FtStm32Project
from FortressTools.projects.qt_project import FtQtProject
from FortressTools.projects.base_project import FtBaseProject
from FortressTools.parser.config.config_parser import ConfigParser
from FortressTools.utils.stm32_utils import FtStm32Utils
from FortressTools.settings.stm32_settings import FtStm32Settings

CONFIG = r"~/.ft/config"

CMD_NONE = 0
CMD_NEW_PROJECT = 1


# TODO
def get_stm32_settings():
    settings = {}
#    settings["name"] = input("Project name: ")
#    settings["stm32_chip"] = input("STM32 Chip: ")
#    settings["stm32cubemx_project"] = input("STM32CubeMX project: ")
    settings["chip"] = "stm32l152re"
    settings["cubemx_project"] = "~/tools/STM32/Projects/STM32CMakeBlink/STM32CMakeBlink.ioc"
    settings["project_template"] = "stm32_blink_project_template.yaml"
    return settings


def get_general_settings():
    settings = {}
    #settings["name"] = input("Project name: ")
    #settings["type"] = input("Project type: ")
    settings["name"] = "TestProject"
    settings["project_type"] = "stm32"
    settings.update(ConfigParser.get_config(CONFIG, settings["project_type"]))
    return settings


def new_project():
    settings = get_general_settings()
    if settings["project_type"] == "cpp":
        settings.update(get_cpp_settings())
        cpp_settings = FtCppSettings()
        for item in settings:
            setattr(cpp_settings, item, settings[item])
        ft_project = FtCppProject(cpp_settings)
    elif settings["project_type"] == "stm32":
        settings.update(get_stm32_settings())
        stm32_settings = FtStm32Settings()
        for item in settings:
            setattr(stm32_settings, item, settings[item])
        ft_project = FtStm32Project(stm32_settings)
    elif settings["project_type"] == "qt":
        settings.update(get_qt_settings())
        qt_settings = FtQtSettings()
        for item in settings:
            setattr(qt_settings, item, settings[item])
        ft_project = FtQtProject(qt_settings)
    else:
        raise Exception()

    ft_project.make()


def main():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument("-n", "--new",
                        action="store_const", dest="command", const=CMD_NEW_PROJECT, required=False,
                        help='Create new project')
    parser.add_argument("-v", "--verbose",
                        action="store_true", dest="verbose", required=False,
                        help='Increase logs verbosity level')
    args = parser.parse_args()

    if args.command == CMD_NEW_PROJECT:
        new_project()
    else:
        pass


if __name__ == "__main__":
    main()
