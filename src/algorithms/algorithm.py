import json

from config import algorithms_path


def get_algorithms() -> dict:
    return json.load(open(algorithms_path, "r", encoding="utf-8"))


def get_algorithm_dict() -> dict:
    algorithms = get_algorithms()

    algo_labels = {}
    for algo_group in algorithms:
        for i in algo_group["children"]:
            algo_labels[i["output_folder"]] = i["label"]
            algo_labels[i["label"]] = i["output_folder"]

    return algo_labels


def get_algorithm_import(algorithm_name: str) -> dict:
    dest = None
    match algorithm_name:
        case "LST":
            from algorithms.GuoHao import LST as dest
        case "SME":
            from algorithms.GuoHao import SME as dest
        case "SWE":
            from algorithms.GuoHao import SWE as dest
        case "AGB" | "SS" | "FVC" | "LAI":
            from algorithms.MaYongGang.run_general import Runner

            dest = Runner(algorithm_name)
        case "lake-chla" | "lake-sdd" | "lake-tsm":
            from algorithms.DuanHongTao.hydro_env import Runner

            dest = Runner(algorithm_name)

    return dest


def run_algorithm(algorithm_name: str) -> dict:
    algo = get_algorithm_import(algorithm_name)

    result = algo.run()

    return result


if __name__ == "__main__":
    print(get_algorithms())
