"""
[directory]
file_landcover    = "I:\7_SoftDev_SWE\20230808\data\MCD12Q1.A2020001.006.LandCoverFractionType1.xinjiang.hdf"
file_snowdensity   = "I:\7_SoftDev_SWE\20230808\data\Monthly_Snow_Density_xinjiang.hdf"
dir_l1r_a   = 'I:\7_SoftDev_SWE\20230808\data\L1R\A'
dir_l1r_d = 'I:\7_SoftDev_SWE\20230808\data\L1R\D'
dir_swe_a = 'I:\7_SoftDev_SWE\20230808\data\SWE\A'
dir_swe_d = 'I:\7_SoftDev_SWE\20230808\data\SWE\D'
[keys]
sdensity = 0.242666
NO_SNOW=6
NO_SCATTER=5
PRECIPITATION=4
COLD_DESERT=3
FROZEN_GROUND=2
SNOW=1
MAX_SNOW_VALUE = 240
UNVALIDATED   = 241
THICK_DRY_SNOW=1
THICK_WET_SNOW=2
THIN_DRY_SNOW=3
THIN_WET_SNOW_or_ForEST_SNOW=4
VERY_THICK_WET_SNOW=5
type=5
[para]
year=2022
month=01
day=01
daynum = 30
latmin = 34
latmax = 50
lonmin = 73
lonmax = 97
resolution = 0.1
flag_default_snow_density = 1
default_snow_depth = 1
[equations]
sd_forest = 'test'
sd_crop = 'test'
sd_grass = 'test'
sd_barren = 'test'

"""

import subprocess
from pathlib import Path
from config import toolbox_path

from .config_writer import write_ini_config

tool_path = toolbox_path / "GuoHao/SWE/xjkk_swe_estimation.exe"


def run(input_path: Path, output_path: Path):
    year, month = input_path.parts[-2:]

    folder_l1r_a = input_path / "L1R" / "A"
    folder_l1r_d = input_path / "L1R" / "D"
    arguments = {}

    arguments["directory"] = {
        "file_landcover": "./static_data/MCD12Q1.A2020001.006.LandCoverFractionType1.xinjiang.hdf",
        "file_snowdensity": "./static_data/Monthly_Snow_Density_xinjiang.hdf",
        "dir_l1r_a": str(folder_l1r_a),
        "dir_l1r_d": str(folder_l1r_d),
        "dir_swe": str(output_path),
    }
    arguments["para"] = {
        "year": year,
        "month": month,
        "latmin": "34",
        "latmax": "50",
        "lonmin": "73",
        "lonmax": "97",
        "resolution": "0.1",
        "flag_default_snow_density": "1",
        "default_snow_depth": "1",
    }
    arguments["keys"] = {
        "sdensity": " 0.242666",
        "NO_SNOW": "6",
        "NO_SCATTER": "5",
        "PRECIPITATION": "4",
        "COLD_DESERT": "3",
        "FROZEN_GROUND": "2",
        "SNOW": "1",
        "MAX_SNOW_VALUE": "240",
        "UNVALIDATED": "241",
        "THICK_DRY_SNOW": "1",
        "THICK_WET_SNOW": "2",
        "THIN_DRY_SNOW": "3",
        "THIN_WET_SNOW_or_ForEST_SNOW": "4",
        "VERY_THICK_WET_SNOW": "5",
        "type": "NO_SCATTER",
    }
    arguments["equations"] = {
        "sd_forest": "test",
        "sd_crop": "test",
        "sd_grass": "test",
        "sd_barren": "test",
    }

    ini_path = write_ini_config(arguments)

    return subprocess.Popen(
        [tool_path, ini_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        cwd=tool_path.parent,
    )


if __name__ == "__main__":
    print("hello world")
