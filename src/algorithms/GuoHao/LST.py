import subprocess
from pathlib import Path
from pprint import pprint
from config import toolbox_path

from .config_writer import write_ini_config

tool_path = toolbox_path / "GuoHao/LST/xjkk_lst_estimation.exe"


def run(input_path: Path, output_path: Path):
    r"""
    [directory]
    dir_L1 = I:/7_SoftDev_LST_EXE/20230808/data/L1/2021/
    file_MERSI24 = I:/7_SoftDev_LST_EXE/20230808/data/AG1KM_EMI_30_180E_0_84N_soil_MERSI24_new.tif
    file_MERSI25 = I:/7_SoftDev_LST_EXE/20230808/data/AG1KM_EMI_30_180E_0_84N_soil_MERSI25_new.tif
    file_LUT = I:/7_SoftDev_LST_EXE/20230808/data/coef1_GSW_SeeBor_Day_LUT4.mat
    dir_LST = I:/7_SoftDev_LST_EXE/20230808/data/LST/2021/
    """
    arguments = {
        "directory": {
            "dir_L1": str(input_path),
            "dir_LST": str(output_path),
            "file_MERSI24": "./static_data/soil_LSE_MERSI24.tif",
            "file_MERSI25": "./static_data/soil_LSE_MERSI25.tif",
            "file_LUT": "./static_data/coef1_gsw_seeBor_day_lut4.mat",
        },
    }

    ini_path = write_ini_config(arguments)
    pprint(arguments)

    return subprocess.Popen(
        [tool_path, ini_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=tool_path.parent,
        encoding="utf-8",
    )


if __name__ == "__main__":
    print("hello world")
