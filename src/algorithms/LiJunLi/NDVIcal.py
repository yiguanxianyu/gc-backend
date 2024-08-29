import subprocess
from pathlib import Path

from config import folder_path, toolbox_path
from utils.util import get_abs_path


def run(params):
    input_path = get_abs_path(params["input"])
    output_path = get_abs_path(params["output"])
    band_red_nir = params["bn"]
    output_dtype = params["output_type"]

    cwd = toolbox_path / "szf" / "MHMapGIS" / "RadiSZF"

    pars = [
        "MHImgNDVIComputeEXE.exe",
        input_path,
        output_path,
        band_red_nir,
        output_dtype,
    ]
    subprocess.run(" ".join(pars), cwd=cwd)

    path = output_path.relative_to(Path(folder_path[0]).parent).as_posix()
    print(path)
    return {"state": "success", "message": "", "label": output_path.name, "path": path}
