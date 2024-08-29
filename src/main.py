from pathlib import Path
from algorithms.algorithm import get_algorithm_import
from api.v1.api import api
from config import debug
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__, static_folder="../dist")
app.register_blueprint(api, url_prefix="/api/v1")

socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("manual-connect")
def handle_connect():
    return "Connection successful, great!"


@socketio.on("run-task")
def handle_task(args):
    print(args)

    input_path = args["path"]
    output_path = input_path.replace("INPUT", "OUTPUT")
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    algo = get_algorithm_import(args["algo-key"])
    process = algo.run(input_path, output_path)

    # import subprocess
    # process = subprocess.Popen(
    #     ["python", "-u", "proc.py"],
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE,
    #     text=True
    # )

    while True:
        output = process.stdout.readline()
        if output.strip() == "" and process.poll() is not None:
            break
        if output:
            print(output, end="")
            socketio.emit("task-process-output", {"data": output, "id": args["id"]})

    rc = process.poll()

    for err in process.stderr.readlines():
        print(err)
        socketio.emit("task-process-output", {"data": err, "id": args["id"]})

    socketio.emit("task-done", {"data": rc, "id": args["id"]})


@app.route("/")
def serve_root():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    CORS(app)
    socketio.run(app, host="0.0.0.0", port=5000, debug=debug)
