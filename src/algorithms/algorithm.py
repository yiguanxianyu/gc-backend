import json
from pathlib import Path

from config import algorithms_path

algorithms = json.load(open(algorithms_path, "r", encoding="utf-8"))

for menuitem in algorithms:
    algorithm_list = menuitem["children"]
    # for al in algorithm_list:
    #     if Path(al["text"]).exists():
    #         # print(al["text"])
    #         with open(al["text"], "r", encoding="utf-8") as file:
    #             # 读取文件内容为字符串
    #             al["text"] = file.read()

del algorithm_list, menuitem

num_algorithms = sum([len(algorithm["children"]) for algorithm in algorithms])


def get_algorithms() -> dict:
    return algorithms


def get_algorithms_count() -> int:
    return num_algorithms


dest = None


def get_algorithm_import(algorithm_name: str) -> dict:
    global dest
    match algorithm_name:
        case "ndvi-calculation":
            from algorithms.LiJunLi import NDVIcal as dest
        case "modis-wt3":
            from algorithms.DuanHongTao import MODIS_WT3 as dest
        case "lake-oacs":
            from algorithms.MaYongGang import Lake_OACs as dest
        case "lst":
            from algorithms.GuoHao import LST as dest
        case "sme":
            from algorithms.GuoHao import SME as dest
        case "swe":
            from algorithms.GuoHao import SWE as dest
        case "lucc":
            from algorithms.LiJunLi import predict_common

            dest = predict_common.Runner(algorithm_name.split("-")[1])

    return dest


def run_algorithm(algorithm_name: str) -> dict:
    algo = get_algorithm_import(algorithm_name)

    result = algo.run()

    return result


if __name__ == "__main__":
    print(algorithms())
