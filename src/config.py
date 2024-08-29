from pathlib import Path

debug = True

raster_ext = [".tif", ".tiff"]
vector_ext = [".shp", ".geojson"]

data_dir = Path(r"C:\Projects\xj_data")
toolbox_path = "./toolbox"
cache_folder_path = "./cache"
algorithms_path = "./data/algo.json"
database_path = "./cache/database.sqlite3"

thumbnail_size = 8000

# 以下部分由程序自动生成，用户无需修改
all_ext = raster_ext + vector_ext

algorithms_path = Path(algorithms_path).absolute()
cache_folder_path = Path(cache_folder_path).absolute()
toolbox_path = Path(toolbox_path).absolute()
database_path = Path(database_path).absolute()

thumb_folder_path = cache_folder_path / "thumbnail"
thumb_folder_path.mkdir(parents=True, exist_ok=True)

input_folder_path = data_dir / "input"
