import tempfile
import time
from configparser import ConfigParser
from pathlib import Path

tempdir = Path(tempfile.gettempdir()) / "GeoComputeEngine"
tempdir.mkdir(parents=True, exist_ok=True)


def write_ini_config(config):
    cf = ConfigParser()
    cf.optionxform = str

    for key, value in config.items():
        cf[key] = value

    time_str = time.strftime(r"%Y-%m-%d-%H-%M-%S", time.localtime())
    file_path = tempdir / f"{time_str}.ini"

    with open(file_path, "w") as f:
        cf.write(f)

    return file_path


if __name__ == "__main__":
    file_path = write_ini_config({"common": {"a": "1", "b": "None"}})

    print(file_path)
    # cf = ConfigParser()
    # cf.read(r"src\algorithms\test.ini")
    # print(type(cf['mysql']['test']))
