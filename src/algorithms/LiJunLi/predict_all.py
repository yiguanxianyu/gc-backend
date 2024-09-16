import subprocess
from pathlib import Path

from config import toolbox_path

tool_path = toolbox_path / "LiJunLi/predict_series_with_mask.py"
model_path = toolbox_path / "LiJunLi/models"


def run(input_path: Path, output_path: Path):
    command = [
        "python",
        "-u",
        str(tool_path),
        "--predict_img_path",
        str(input_path),
        "--output_path",
        str(output_path),
        "--model_path",
        str(model_path),
    ]

    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tool_path.parent,
        text=True,
        encoding="gbk",
    )
