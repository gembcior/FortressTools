import argparse
from fortress_tools.projects.cpp_project import FtCppProject
from fortress_tools.projects.stm32_project import FtSTM32Project
from fortress_tools.projects.qt_project import FtQtProject
from fortress_tools.projects.base_project import FtBaseProject
import os


def main():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument("-n", "--name",
                        action="store", dest="project_name", default="NewFtProject", required=False,
                        help='Project name')
    parser.add_argument("-w", "--workspace",
                        action="store", dest="project_workspace", default="current", required=False,
                        help='Project workspace')
    parser.add_argument("-t", "--type",
                        action="store", dest="project_type", default="cpp", required=False,
                        help='Project type')
    args = parser.parse_args()

    if args.project_workspace == "current":
        path = os.getcwd()
    else:
        path = os.path.abspath(args.project_workspace)

    settings = {}
    settings["name"] = args.project_name
    settings["workspace"] = path
    settings["templates"] = os.path.abspath("/home/tgebka/workspace/FortressTools/templates")
    settings["verbose"] = True
    settings["stm32cubemx"] = os.path.abspath("/home/tgebka/tools/STM32/STM32CubeMX/STM32CubeMX")
    settings["stm32cubemx_project"] = os.path.abspath("/home/tgebka/workspace/cubemx.ioc")
    settings["stm32cube"] = os.path.abspath("/home/tgebka/tools/STM32/STM32Cube/STM32Cube_FW_F4_V1.25.0")
    settings["toolchain"] = os.path.abspath("/home/tgebka/tools/toolchain/gcc-arm-none-eabi-9-2019-q4-major")
    settings["stm32_chip"] = "stm32f411"
    settings["stm32_family"] = "f4"
    settings["stm32_chip_type"] = "xe"


    if args.project_type == "cpp":
        ft_project = FtCppProject(settings)
    elif args.project_type == "stm32":
        ft_project = FtSTM32Project(settings)
    elif args.project_type == "qt":
        ft_project = FtQtProject(settings)
    else:
        ft_project = FtCppProject(settings)

    ft_project.make()


if __name__ == "__main__":
    main()
