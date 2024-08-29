import subprocess
from pathlib import Path

from config import folder_path, toolbox_path

base_data_path = Path(folder_path[0])

tool_path = toolbox_path / "DuanHongTao" / "MODIS_WT3" / "MODIS_WT3.py"
surface_ref_path = (
    base_data_path / "Water" / "lake_surface_temperature" / "surafce_reflectance"
)
temperature_path = base_data_path / "Water" / "lake_surface_temperature" / "temperature"
output_path = base_data_path / "Water" / "lake_surface_temperature" / "output"

output_path.mkdir(parents=True, exist_ok=True)


def get_parameters():
    arguments = {}
    arguments["-r"] = next(
        (str(item) for item in surface_ref_path.iterdir() if item.is_dir()), None
    )
    arguments["-t"] = next(
        (str(item) for item in temperature_path.iterdir() if item.is_dir()), None
    )
    arguments["-o"] = str(output_path)

    lack_para = [i for i in arguments.keys() if arguments[i] is None]

    return arguments, lack_para


def run():
    arguments, lack_para = get_parameters()

    # if len(lack_para) != 0:
    #     return {"state": "error", "message": "参数不完整,缺少文件（或文件夹）参数：" + ",".join(lack_para)}

    process_args = [
        "python",
        "-u",
        tool_path,
        "-r",
        arguments["-r"],
        "-t",
        arguments["-t"],
        "-o",
        arguments["-o"],
    ]

    return subprocess.Popen(
        process_args, stdout=subprocess.PIPE, text=True, encoding="utf-8"
    )


# # 脚本输入参数
# parser = argparse.ArgumentParser()
# parser.add_argument('-r', '--dirsr', required=True, type=Path)
# parser.add_argument('-t', '--dirst', required=True, type=Path)
# parser.add_argument('-m', '--month', type=str)
# parser.add_argument('-o', '--output', required=True, type=Path)
# args = parser.parse_args()
