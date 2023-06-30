# multi_gen.py
# Chet Russell
# Last edited: 6/30/2023
#
# This file generates a multispectral orthomosaic using images from a Micasense
# RedEdge-MX multispectral camera. It has not been tested on other camera
# models, but probably still works fine on them? To run this code you must have
# Open Drone Map installed locally on windows:
# https://github.com/OpenDroneMap/ODM/releases
#
# Note: the generation of a multispectral orthomosaic is very processing-heavy,
# so the settings I have set in here generate a worse quality ortho, for the
# sake of our poor computer. If you find yourself having memory issues, reduce
# the quality of pc_quality and feature_quality.

import yaml
import os

data = {
    "project_path": "",
    "orthophoto_cutline": False,
    # "min_num_features": 20000,
    # "dem_decimation": 50,
    "pc_quality": "medium",
    "feature_quality": "medium",
    "texturing_data_term": "gmi",
    "verbose": True,
    "time": True,
    "crop": 0,
    "auto_boundary": False,
    "skip_3dmodel": True,
    "cog": False,
    "use_3dmesh": False,
    "pc_tile": True,
    "orthophoto-kmz": False,
    "use_exif": True,
    "orthophoto_resolution": 1,
    "no_gpu": False,
    # "ignore_gsd": False,
    "fast_orthophoto": True,
    "feature-type": "sift",
    "radiometric_calibration": "camera",
    # "split": 500,
    # "split_overlap": 100,
    "optimize_disk_space": True,
    "resize-to": -1,
    "merge": "orthophoto",
    # "primary_band": "NIR",
}

yaml_output = yaml.dump(data, sort_keys=False)

print(yaml_output)


def write_yaml_to_file(py_obj, filename):
    with open(
        f"{filename}.yaml",
        "w",
    ) as f:
        yaml.dump(py_obj, f, sort_keys=False)
    print("Written to file successfully")


# This should contain the path to your ODM installation, specifically pointing towards the settings.yaml file.
write_yaml_to_file(data, "C:\\ODM\\settings")

# This should contain the path to your ODM installation, specifically pointing towards the run.bat file.
os.system("C:\\ODM\\run.bat")
