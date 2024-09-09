import subprocess
from pathlib import Path

from config import toolbox_path


class Runner:
    def __init__(self, algorithm_name: str):
        match algorithm_name:
            case "lake-chla":
                self.tool_path = (
                    toolbox_path / "DuanHongTao/hydroenv/rf_msi_chla_pred.py"
                )
            case "lake-sdd":
                self.tool_path = (
                    toolbox_path / "DuanHongTao/hydroenv/rf_msi_sdd_pred.py"
                )
            case "lake-tsm":
                self.tool_path = (
                    toolbox_path / "DuanHongTao/hydroenv/rf_msi_tsm_pred.py"
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


# # 脚本输入参数
# parser = argparse.ArgumentParser()
# parser.add_argument('-r', '--dirsr', required=True, type=Path)
# parser.add_argument('-t', '--dirst', required=True, type=Path)
# parser.add_argument('-m', '--month', type=str)
# parser.add_argument('-o', '--output', required=True, type=Path)
# args = parser.parse_args()
