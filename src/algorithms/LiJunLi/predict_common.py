import subprocess

from config import folder_path, toolbox_path

tool_path = toolbox_path / "LiJunLi/AGRS_semantic_segmentation_240521/predict.py"

folder = folder_path[0] / "地表覆盖要素"

pred_img_dir = folder / "1-test_img"


class Runner:
    def __init__(self, type):
        self.type = type

    def run(self):
        train_list_dir = folder / self.type / "2-trainlist"
        train_list_path = next(train_list_dir.glob("*.txt"), None)

        model_dir = folder / self.type / "3-weights"
        model_path = next(model_dir.glob("*.th"), None)

        output_path = folder / self.type / "4-predict_result"
        output_path.mkdir(parents=True, exist_ok=True)

        output = subprocess.run(
            [
                "python",
                str(tool_path),
                "--predictImgPath",
                str(pred_img_dir),
                "--trainListRoot",
                str(train_list_path),
                "--model_path",
                str(model_path),
                "--output_path",
                str(output_path),
            ],
            capture_output=True,
            text=True,
        )

        return output.stdout


if __name__ == "__main__":
    print("hello world")
