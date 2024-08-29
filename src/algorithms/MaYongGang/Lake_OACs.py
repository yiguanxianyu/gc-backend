import subprocess
from pathlib import Path

from config import folder_path, toolbox_path

base_data_path = Path(folder_path[0])

tool_path = toolbox_path / "MaYongGang" / "lake_OACs" / "Lake_OACs.py"
input = base_data_path / "Ecology" / "OACs" / "input"
output = base_data_path / "Ecology" / "OACs" / "output"
output.mkdir(parents=True, exist_ok=True)


def run():
    process_args = ["python", tool_path, "-i", input, "-o", output]
    print("OACs start", process_args)
    result = subprocess.run(process_args, text=True, capture_output=True)
    print("OACs finished")

    return {"state": "success", "message": "程序运行完成"}


# # 脚本输入参数
# parser = argparse.ArgumentParser()
# parser.add_argument('-r', '--dirsr', required=True, type=Path)
# parser.add_argument('-t', '--dirst', required=True, type=Path)
# parser.add_argument('-m', '--month', type=str)
# parser.add_argument('-o', '--output', required=True, type=Path)
# args = parser.parse_args()
