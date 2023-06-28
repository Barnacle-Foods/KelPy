import yaml
import os

data = {
    "project_path": "C:\\Users\\matt\\Documents\\GitHub\\New-ortho\\tlt",
    "orthophoto_cutline": True,
    #"min_num_features": 20000,
    #"dem_decimation": 50,
    "pc_quality": "medium",
    "feature_quality": "high",
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
    #"ignore_gsd": False,
    "fast_orthophoto": True,
    "feature-type": "sift",
    "radiometric_calibration": "camera",
    #"split": 500,
    #"split_overlap": 100,
    "optimize_disk_space": True,
    "resize-to": -1,
    "merge": "orthophoto",
    } 

yaml_output = yaml.dump(data, sort_keys=False) 

print(yaml_output) 

def write_yaml_to_file(py_obj, filename):
    with open(f'{filename}.yaml', 'w',) as f :
        yaml.dump(py_obj,f,sort_keys=False) 
    print('Written to file successfully')

write_yaml_to_file(data, 'C:\\Users\\matt\\Documents\\GitHub\\barnacle-imagery\\ODM\\settings')

    
for file in os.listdir("C:\\Users\\matt\\Documents\\GitHub\\New-ortho\\tlt\\code\\images"):
    filename = os.fsdecode(file)
    #print(filename)
    #print(filename[-5:])
    if filename[-5:] == "3.tif" or filename[-5:] == "4.tif":
        continue 
    else:
        os.remove("C:\\Users\\matt\\Documents\\GitHub\\New-ortho\\tlt\\code\\images\\" + filename)

os.system('C:\\Users\\matt\\Documents\\GitHub\\barnacle-imagery\\ODM\\run.bat')