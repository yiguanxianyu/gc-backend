"""
参数说明：

sigma   ： 存放sigma的文件夹
pmwmax  ： 存放pasmax的文件夹
pmwmin  ： 存放pasmin的文件夹
sme     ： 存放输出的sme的文件夹
dateinfo： 存放日期信息mat文件的文件夹
"""

import subprocess
from pathlib import Path

from config import toolbox_path

from .config_writer import write_ini_config

tool_path = toolbox_path / "GuoHao/SME/xjkk_sme.exe"


def run(input_path: Path, output_path: Path):
    folder_sigma = input_path / "sigma"
    folder_pasmax = input_path / "pmwmax"
    folder_pasmin = input_path / "pmwmin"
    folder_sme = output_path
    folder_dateinfo = input_path / "mat"

    arguments = {
        "directory": {
            "dir_sigma": str(folder_sigma),
            "dir_pasmax": str(folder_pasmax),
            "dir_pasmin": str(folder_pasmin),
            "dir_sme": str(folder_sme),
            "mat_dateinfo": str(next(folder_dateinfo.glob("*.mat"), None)),
        },
    }

    ini_path = write_ini_config(arguments)

    return subprocess.Popen(
        [tool_path, ini_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=tool_path.parent,
        encoding="utf-8",
    )


# if __name__ == "__main__":
#     print("hello world")

# def get_parameters():
#     arguments = {}
#     arguments_directory = {}

#     arguments_directory["dir_sigma"] = str(folder_sigma.resolve())
#     arguments_directory["dir_pasmax"] = str(folder_pasmax.resolve())
#     arguments_directory["dir_pasmin"] = str(folder_pasmin.resolve())
#     arguments_directory["dir_sme"] = str(folder_sme.resolve())
#     arguments_directory["mat_dateinfo"] = str(next(folder_dateinfo.glob("*.mat"), None))

#     arguments["directory"] = arguments_directory

#     lack_para = [
#         i for i in arguments_directory.keys() if arguments_directory[i] is None
#     ]
# if len(lack_para) != 0:
#     return {
#         "state": "error",
#         "message": "参数不完整,缺少文件（或文件夹）参数：" + ",".join(lack_para),
#     }
#     return arguments, lack_para
