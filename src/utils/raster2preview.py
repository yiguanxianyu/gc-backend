import subprocess
from uuid import uuid4

import rasterio
from pyproj import Transformer
from rasterio.enums import ColorInterp
from pathlib import Path
from config import thumb_folder_path, thumbnail_size
from database import db_handler


def raster2preview_(input_tiff):
    input_tiff = str(input_tiff)
    if result := db_handler.get_thumb(input_tiff):
        uuid = result[0]
        if (thumb_folder_path / f"{uuid}.jpg").exists():
            extent = result[1:]
            return extent, uuid

    outband = ""
    expand = ""
    scale = "-scale"

    with rasterio.open(input_tiff) as dataset:
        band_count = dataset.count
        color = dataset.colorinterp
        input_width = dataset.width
        input_height = dataset.height
        bounds = dataset.bounds

        if band_count == 1:
            if color[0] == ColorInterp.palette:
                expand = "-expand rgb"
                scale = ""
        elif band_count == 2:
            outband = "-b 1 -b 2 -b 2"
        elif band_count >= 3:
            try:
                red_ = color.index(ColorInterp.red)
                green_ = color.index(ColorInterp.green)
                blue_ = color.index(ColorInterp.blue)
                outband = "-b {} -b {} -b {}".format(red_ + 1, green_ + 1, blue_ + 1)
            except ValueError:
                outband = "-b 1 -b 2 -b 3"

        trans = Transformer.from_crs(str(dataset.crs), "EPSG:3857", always_xy=True)
        extent = trans.transform_bounds(
            bounds.left, bounds.bottom, bounds.right, bounds.top
        )

        outsize = ""
        if max(input_width, input_height) > thumbnail_size:
            if input_width > input_height:
                out_w, out_h = thumbnail_size, 0
            else:
                out_w, out_h = 0, thumbnail_size
            outsize = "-outsize {} {}".format(out_w, out_h)

    uuid = str(uuid4())
    pars = ["gdal_translate.exe"]
    pars.append("-r  nearest")
    pars.append("-ot Byte")
    pars.append("-oo NUM_THREADS=4")
    pars.append("-co QUALITY=85")
    pars.append("--config GDAL_PAM_ENABLED NO")

    pars.append(scale)
    pars.append(outsize)
    pars.append(outband)
    pars.append(expand)
    pars.append(input_tiff)
    pars.append("{}/{}.jpg".format(str(thumb_folder_path), uuid))
    subprocess.run(" ".join(pars))

    db_handler.insert_thumb(input_tiff, uuid, extent)
    return raster2preview_(input_tiff)


def get_tiff_extent(input_tiff: Path):
    with rasterio.open(input_tiff) as dataset:
        bounds = dataset.bounds
        trans = Transformer.from_crs(str(dataset.crs), "EPSG:3857", always_xy=True)
        extent = trans.transform_bounds(
            bounds.left, bounds.bottom, bounds.right, bounds.top
        )
        return extent


def get_preview(input_tiff: Path):
    for suffix in [".png", ".jpg", ".jpeg"]:
        preview_path = input_tiff.with_suffix(suffix)
        if preview_path.exists():
            return preview_path
