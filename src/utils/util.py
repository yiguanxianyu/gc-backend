import json
import subprocess
from pathlib import Path

import psutil
import pynvml
import rasterio
from pyproj import Transformer
from send2trash import send2trash

import config

try:
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    has_nvidia_gpu = True
except Exception:
    has_nvidia_gpu = False


def get_tiff_extent(input_tiff: Path):
    with rasterio.open(input_tiff) as dataset:
        bounds = dataset.bounds
        trans = Transformer.from_crs(dataset.crs, "EPSG:3857", always_xy=True)
        extent = trans.transform_bounds(
            bounds.left, bounds.bottom, bounds.right, bounds.top
        )
    return extent


def get_preview(input_tiff: Path):
    for suffix in [".png", ".jpg", ".jpeg"]:
        preview_path = input_tiff.with_suffix(suffix)
        if preview_path.exists():
            return preview_path


def is_raster(path):
    return Path(path).suffix.lower() in config.raster_ext


def is_vector(path):
    return Path(path).suffix.lower() in config.vector_ext


def get_abs_path(path):
    return config.data_dir.parent / path


def read_text(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        text = str(e)

    return text


def generate_file_tree(root_dir):
    def scan_directory(directory):
        tree = {
            "key": directory.resolve().as_posix(),
            "label": directory.name,
            "children": [],
        }
        for path in directory.iterdir():
            if path.is_dir():
                subtree = scan_directory(path)
                if subtree["children"]:  # Only add directory if it contains tif files
                    tree["children"].append(subtree)
            elif path.suffix == ".tif":
                tree["children"].append(
                    {
                        "key": path.resolve().as_posix(),
                        "label": path.name,
                    }
                )
            elif path.name == "info.txt":
                tree["text"] = read_text(path.resolve())
        return tree

    file_tree = scan_directory(Path(root_dir))
    return file_tree["children"]


def get_directory_new(algorithms):
    data_dir = {}
    root = Path(config.data_dir) / "output"

    for algorithm_group in algorithms:
        path_group = Path(algorithm_group["folder"])
        for algorithm in algorithm_group["children"]:
            dir = root / path_group / algorithm["folder"]
            tree = generate_file_tree(dir)

            data_dir[algorithm["key"]] = tree

    return data_dir


depth_data = ["blank", "year", "month", "day", "hour", "minute", "second"]


def generate_input_tree(algorithms):
    info_txt_dict = {}

    def scan_directory(dir, depth):
        tree = {
            "value": dir.resolve().as_posix(),
            "label": dir.name,
        }
        if depth == 0:
            info_txt_dict[dir.resolve().as_posix()] = read_text(dir / "info.txt")
            return tree
        for path in dir.iterdir():
            if path.is_dir():
                subtree = scan_directory(path, depth - 1)
                tree.setdefault("children", []).append(subtree)
        return tree

    input_data = {}
    root = Path(config.data_dir) / "INPUT"

    for algorithm_group in algorithms:
        path_group = root / algorithm_group["folder"]
        for algorithm in algorithm_group["children"]:
            dir = path_group / algorithm["folder"]
            depth = depth_data.index(algorithm["timeType"])
            tree = scan_directory(dir, depth)
            input_data[algorithm["key"]] = tree.setdefault("children", [])

    # print(input_data)
    return input_data, info_txt_dict


def rename_path(old_path, new_name):
    dest_path = get_abs_path(old_path)
    Path(dest_path).rename(dest_path.parent / new_name)


def remove_path(file_path):
    dest_path = get_abs_path(file_path)
    print("Removing:", dest_path)
    send2trash(dest_path)


def get_file_list(path: str):
    path = Path(path) / "output"
    return [{"label": i.name, "value": i.name} for i in path.glob("*.tif")]


def get_system_utilization():
    # gpu_usage = pynvml.nvmlDeviceGetUtilizationRates(handle)

    # total_used_space = 0
    # total_capacity = 0

    # for partition in psutil.disk_partitions():
    #     if len(str(partition.mountpoint)) != 3:
    #         continue
    #     # 获取分区使用情况
    #     usage = psutil.disk_usage(partition.mountpoint)
    #     # 累加分区容量和使用量
    #     total_used_space += usage.used
    #     total_capacity += usage.total

    # disk_usage = total_used_space / total_capacity * 100

    if has_nvidia_gpu:
        gpu_usage = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=utilization.gpu",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
        ).stdout.replace("\n", "")
        gpu_usage_value = float(gpu_usage)

        gpu_memory = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=memory.used,memory.total",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
        ).stdout.replace("\n", "")
        gpu_memory = gpu_memory.split(", ")
        gpu_usage_memory_value = round(
            float(gpu_memory[0]) / float(gpu_memory[1]) * 100
        )

    else:
        gpu_usage_value = "N/A"
        gpu_usage_memory_value = "N/A"

    result = {
        "cpuUsage": round(psutil.cpu_percent()),
        "memoryUsage": round(psutil.virtual_memory().percent),
        "gpuUsage": gpu_usage_value,
        "gpuMemoryUsage": gpu_usage_memory_value,
        # "numImages": get_file_count("raster"),
        # "numVectors": get_file_count("vector"),
        # "numAlgorithms": get_algorithms_count(),
        # "diskUsage": round(disk_usage),
    }

    return result


# def raster2preview_legacy(input_tiff):
#     if (result := db_handler.get_thumb(input_tiff.as_posix())):
#         uuid = result[0]
#         if Path(thumb_folder_path, f"{uuid}.png").exists():
#             extent = result[1:]
#             return extent, uuid

#     uuid = str(uuid4())
#     dataset = rasterio.open(input_tiff)

#     num_bands = dataset.count
#     input_width = dataset.width
#     input_height = dataset.height

#     if num_bands == 1:
#         png_band = [1]
#     elif num_bands == 2:
#         png_band = [1, 2, 2]
#     else:
#         png_band = [1, 2, 3]

#     resample_factor = 1
#     if (max_length := max(input_width, input_height)) > thumbnail_size:
#         resample_factor = thumbnail_size / max_length

#     # 输出宽高
#     output_width = int(input_width * resample_factor)
#     output_height = int(input_height * resample_factor)

#     with rasterio.open(f"{thumb_folder_path}/{uuid}.png",
#                        'w',
#                        width=output_width,
#                        height=output_height,
#                        driver="png",
#                        count=len(png_band),
#                        dtype="uint8",
#                        nodata=dataset.nodata) as new:

#         for band_index, index in enumerate(png_band, 1):
#             arr = dataset.read(band_index,
#                                masked=True,
#                                out_shape=(output_width, output_height),
#                                resampling=rasterio.enums.Resampling.nearest).astype(np.float32)

#             arr_min, arr_max = np.min(arr), np.max(arr)
#             if arr_min != arr_max:
#                 arr = np.round(255 * (arr - arr_min) / (arr_max - arr_min))

#             new.write(arr.data.astype(np.uint8), index)

#     bounds = dataset.bounds
#     trans = Transformer.from_crs(str(dataset.crs), "EPSG:3857", always_xy=True)
#     dataset.close()

#     extent = trans.transform_bounds(bounds.left, bounds.bottom, bounds.right, bounds.top)
#     db_handler.insert_thumb(input_tiff.as_posix(), uuid, extent)
#     return raster2preview(input_tiff)
#     # print(extent, dataset.bounds, dataset.crs)
#     # return extent, uuid

# def get_directory_legacy():

#     def generate_tree(folder, include_extensions):

#         def _generate_tree(path):
#             if path.is_file() and path.suffix.lower() not in include_extensions:
#                 return None

#             node = {'label': path.name, 'path': path.relative_to(folder.parent).as_posix()}

#             if path.is_dir():
#                 children = [_generate_tree(child) for child in path.iterdir()]
#                 children = [child for child in children if child is not None]  # Remove None values
#                 node['children'] = children
#             return node

#         folder = Path(folder)
#         tree = _generate_tree(folder)
#         return tree

#     return [generate_tree(folder, all_ext) for folder in folder_path]


# def get_directory(algorithms):
#     def generate_tree(folder):
#         def _generate_tree(path):
#             children = [
#                 _generate_tree(child) for child in path.iterdir() if (child.is_dir() and child.name != "input")
#             ]

#             if info_json.exists():
#                 info = json.load(open(info_json, "r", encoding="utf-8"))
#                 node = {"label": info[path.name]}
#             else:
#                 node = {"label": path.name}
#             if children:
#                 node["children"] = children

#             node["value"] = path.relative_to(folder.parent).as_posix()
#             return node

#         folder = Path(folder)
#         tree = _generate_tree(folder)
#         return tree

#     output = [generate_tree(folder) for folder in config.data_dir.iterdir() if folder.is_dir()]
#     print(output)
#     return output


# def get_directory_legacy():
#     def generate_tree(folder):
#         def _generate_tree(path):
#             node = {
#                 "label": path.name,
#                 "value": path.relative_to(folder.parent).as_posix(),
#             }

#             if path.is_dir():
#                 children = [_generate_tree(child) for child in path.iterdir()]
#                 children = [child for child in children if child is not None]  # Remove None values
#                 node["children"] = children

#             else:
#                 if path.suffix.lower() not in config.raster_ext:
#                     node = None

#             return node

#         folder = Path(folder)
#         tree = _generate_tree(folder)
#         return tree

#     output = [generate_tree(folder) for folder in config.data_dir.iterdir()]
#     print(output)
#     return output


# def get_file_count(type):
#     count = 0
#     if type == "raster":
#         for ext in raster_ext:
#             for folder in folder_path:
#                 count += len(list(Path(folder).rglob("**/*" + ext)))
#     elif type == "vector":
#         for ext in vector_ext:
#             for folder in folder_path:
#                 count += len(list(Path(folder).rglob("**/*" + ext)))
#     else:
#         raise Exception("Unknown file type")

#     return count
