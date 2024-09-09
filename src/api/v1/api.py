import json
from pathlib import Path

from flask import Blueprint, jsonify, request, send_file

from algorithms.algorithm import get_algorithms, get_algorithm_dict
from utils.raster2preview import get_tiff_extent
from utils.util import (
    generate_input_tree,
    get_directory_new as get_directory,
    get_file_list,
    get_system_utilization,
    remove_path,
)

api = Blueprint("item", __name__)


@api.route("/get/monitor", methods=["GET"])
def get_monitor():
    result = get_system_utilization()
    return jsonify(result)


@api.route("/get/thumbnail/", methods=["GET"])
def get_thumbnail():
    """{
        "path": path,
    }"""
    path = request.args.get("path")
    thumbnail_path = Path(path).with_suffix(".png")
    return send_file(thumbnail_path)


@api.route("/get/iteminfo/", methods=["GET"])
def get_item_info():
    """{
        "path": "UAV_DATA_NEW/1_erosion/061301_result_erosion.tif",
    }"""
    path = request.args.get("path")
    extent = get_tiff_extent(path)
    return jsonify(
        {
            "status": "success",
            "extent": extent,
        }
    )


@api.route("/get/directory/output", methods=["GET"])
def get_dir_output():
    algos = get_algorithms()
    result = get_directory(algos)
    return jsonify(result)


@api.route("/get/directory/input", methods=["GET"])
def get_dir_input():
    algos = get_algorithms()
    result = generate_input_tree(algos)
    return jsonify(result)


@api.route("/get/filelist/", methods=["GET"])
def get_test():
    path = request.args.get("path")
    result = get_file_list(path)
    return jsonify(result)


@api.route("/get/algorithms/", methods=["GET"])
def get_algo():
    result = get_algorithms()
    return jsonify(result)


@api.route("/get/algorithms_dict/", methods=["GET"])
def get_algo_dict():
    result = get_algorithm_dict()
    return jsonify(result)


@api.route("/post/remove", methods=["POST"])
def post_remove():
    data = request.get_json()
    result = remove_path(data["path"])
    return jsonify(result)


# @api.route("/post/rename", methods=["POST"])
# def post_rename():
#     data = request.get_json()
#     result = rename_path(data["path"], data["new-name"])
#     return jsonify(result)


# @api.route("/post/run", methods=["POST"])
# def post_run_algo():
#     data = request.get_json()
#     print(data)

#     result = run_algorithm(data["algo-key"])

#     if result["state"] == "error":
#         status_code = 500
#     else:
#         status_code = 200

#     return jsonify(result), status_code

# @api.route("/get/thumbnail/", methods=["GET"])
# def get_thumbnail():
#     """{
#         "thumbnailId": uuid,
#     }"""
#     uuid = request.args.get("thumbnailId")
#     thumbnail_path = thumb_folder_path / f"{uuid}.jpg"
#     return send_file(thumbnail_path, mimetype="image/jpg")


# @api.route("/get/ovr/", methods=["GET"])
# def get_overview():
#     """{
#         "thumbnailId": uuid,
#     }"""
#     uuid = request.args.get("thumbnailId")
#     thumbnail_path = thumb_folder_path / f"{uuid}.tif.ovr"
#     return send_file(thumbnail_path)
