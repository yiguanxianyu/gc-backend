import subprocess
from pathlib import Path

from config import toolbox_path


class Runner:
    def __init__(self, algorithm_name: str):
        match algorithm_name:
            case "LAI":
                self.tool_path = (
                    toolbox_path / "MaYongGang/LAI(叶面积指数)/main_interface.py"
                )
            case "SS":
                self.tool_path = (
                    toolbox_path / "MaYongGang/SS(土壤盐分)/main_interface.py"
                )
            case "FVC":
                self.tool_path = (
                    toolbox_path / "MaYongGang/FVC(植被覆盖度)/main_interface.py"
                )
            case "AGB":
                self.tool_path = (
                    toolbox_path / "MaYongGang/AGB(地上生物量)/main_interface.py"
                )

    def run(self, input_path: Path, output_path: Path):
        command = ["python", "-u", self.tool_path, "-i", input_path, "-o", output_path]

        return subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.tool_path.parent,
            text=True,
            encoding="gbk",
        )
