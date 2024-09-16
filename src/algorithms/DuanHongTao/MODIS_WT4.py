import subprocess
from pathlib import Path

from config import toolbox_path

tool_path = toolbox_path / "DuanHongTao/hydrotemp/MODIS.WT4.py"


def run(input_path: Path, output_path: Path):
    command = [
        "python",
        "-u",
        tool_path,
        "-r",
        input_path / "MYD09A1",
        "-t",
        input_path / "MYD11A2",
        "-o",
        output_path,
    ]

    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tool_path.parent,
        text=True,
        encoding="gbk",
    )
