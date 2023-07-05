# Kelpy core file
# File created: 6/28/2022
# Author: Chet Russell
# Last edited: 6/26/2023 - Chet Russell

import os
import shutil
import PyPDF2
import kelp_o_matic
import rasterio
import glint_mask_tools
from PIL import Image
import yaml
import tempfile
import gui
import glob

""" ------------------------ MASKER FUNCTION ---------------------------
This function takes an image directory and a pixel buffer and runs the
glint-mask-tools python package.
:param imgdir: The directory where the images are stored.
:param pb: The value the glint-mask-tools package takes when calculating
           pixels affected.
------------------------------------------------------------------------ """


def masker(imgdir: str, pb: int):
    # This is the function that creates the image mask using glint-mask-tools.
    masker = glint_mask_tools.RGBThresholdMasker(
        img_dir=imgdir, mask_dir=imgdir, pixel_buffer=pb
    )
    masker.__call__(max_workers=0, callback=print, err_callback=print)

    # This turns the mask files from .png to .jpg
    for filename in os.listdir(imgdir):
        infilename = os.path.join(imgdir, filename)
        if not os.path.isfile(infilename):
            continue
        # oldbase = os.path.splitext(filename)
        newname = infilename.replace(".png", ".JPG")
        os.rename(infilename, newname)


""" --------------------- ORTHORECTIFICATION FUNCTION ---------------------- 
This function takes an image directory, a results directory, a quality value,
a crop value, a kmz boolean value and an exif boolean value. It takes all of
these values and runs the ODM (Open-Drone-Map) create_task function in a
docker container. https://docs.opendronemap.org/

:param imgdir: The directory where the images are stored.

:param dwndir: The directory where the results are stored.

:param quality: ODM option to determine quality of the orthomosaic generated.
                More info: https://docs.opendronemap.org/arguments/pc-quality/

:param crop: ODM option to crop dataset boundaries. More info:
             https://docs.opendronemap.org/arguments/crop/

:param kmz: ODM option to return Google Earth (kmz) file. More info:
            https://docs.opendronemap.org/arguments/orthophoto-kmz/

:param ft: ODM option to determine feature types. More info:
           https://docs.opendronemap.org/arguments/feature-type/

:param exif: ODM option to use EXIF information on images. More info:
             https://docs.opendronemap.org/arguments/use-exif/

:param pb: The value the glint-mask-tools package takes when calculating
           pixels affected.
------------------------------------------------------------------------ """


def orthorec(
    imgdir: str,
    dwndir: str,
    quality: str,
    crop: int,
    kmz: bool,
    ft: str,
    exif: bool,
    pb: int,
):
    imglist = []

    # Places each image filepath into the imglist list.
    for filenames in os.listdir(imgdir):
        tmp = imgdir + "/" + filenames
        imglist.append(tmp)

    # Using a temporary directory to store all files associated with OpenDroneMap
    with tempfile.TemporaryDirectory() as tmpdirname:
        print("created temporary directory", tmpdirname)

        # Weird OpenDroneMap things...
        tmpimgs = tmpdirname + "\\code\\images"
        os.mkdir(tmpdirname + "\\code")
        os.mkdir(tmpimgs)

        # Copying all images from image folder to new tmp directory
        for jpgfile in glob.iglob(os.path.join(imgdir, "*.jpg")):
            shutil.copy(jpgfile, tmpimgs)

        # Creating glint masks
        masker(tmpimgs, pb)

        # Creating a dictionary to store the .yaml information
        data = {
            "project_path": tmpdirname,
            "orthophoto_cutline": False,
            "min_num_features": 20000,
            "pc_quality": quality,
            "texturing_data_term": "gmi",
            "verbose": True,
            "time": True,
            "crop": crop,
            "auto_boundary": False,
            "skip_3dmodel": True,
            "cog": False,
            "use_3dmesh": False,
            "pc_tile": True,
            "orthophoto_kmz": kmz,
            "use_exif": exif,
            "orthophoto_resolution": 1,
            "no_gpu": False,
            "ignore_gsd": False,
            "fast_orthophoto": True,
            "feature_type": ft,
        }

        yaml_output = yaml.dump(data, sort_keys=False)

        print(yaml_output)

        # yaml file to run OpenDroneMap
        def write_yaml_to_file(py_obj, filename):
            with open(
                f"{filename}.yaml",
                "w",
            ) as f:
                yaml.dump(py_obj, f, sort_keys=False)
            print("Written to file successfully")

        write_yaml_to_file(data, gui.resource_path("ODM\\settings"))

        # Running OpenDroneMap on windows natively (without Docker!!!)
        os.system(gui.resource_path("ODM\\run.bat"))

        # Grab the pdf and tif file and send them to the download folder
        extract_essentials(tmpdirname, dwndir)

        # Creating a viewable jpg so you can see what the tif looks like. This is really only necessary when you are dealing with gigantic tif files.
        compress_tif(dwndir + "/odm_orthophoto.tif", dwndir + "/viewableOrtho.jpg")


""" ---------------------- SEGMENTATION FUNCTION --------------------------- 
This function takes an orthomosaic file, the path for a tif file,
a GSD (ground sampling distance) and a species classification boolean.
It takes the raster tif generated by the find_kelp function in the
hakai_segmentation package and uses that to create a colormap file. This
colormap is a tif file that has 2 colors, one color designating kelp and one
color designating the lack of kelp. It then spits out area calculations.

:param ortho: The path where the orthomosaic image is stored.
:param komp: The directory that the kelpomatic image will be placed in.
:param gsd: The ground sampling distance calculation.
:param spec: Whether kelpomatic should attempt to identify kelp species.
------------------------------------------------------------------------ """


def seg(ortho: str, komp: str, gsd: float, spec: bool):
    Image.MAX_IMAGE_PIXELS = 9999999999
    kelp = 0
    no_kelp = 0
    bull = 0
    giant = 0

    kom = komp + "/kelpomatic.tif"
    ext1 = ""
    ext2 = ""

    if spec == False or spec == "0":
        ext1 = "\\colormap.tif"
        ext2 = "\\kelp_area.txt"
    elif spec == True or spec == "1":
        ext1 = "\\species_colormap.tif"
        ext2 = "\\species_kelp_area.txt"

    # Calling the kelpomatic tool
    kelp_o_matic.find_kelp(ortho, kom, species=spec, use_gpu=True)

    # Writing the colormap
    with rasterio.Env():
        with rasterio.open(kom) as src:
            shade = src.read(1)
            meta = src.meta

        with rasterio.open(komp + ext1, "w", **meta) as dst:
            dst.write(shade, indexes=1)
            # If species differentiation is turned off
            if spec == False or spec == "0":
                dst.write_colormap(
                    1,
                    {
                        0: (0, 0, 255, 255),
                        1: (255, 255, 0, 255),
                    },
                )
            # If species differentiation is turned on
            elif spec == True or spec == "1":
                dst.write_colormap(
                    1,
                    {
                        0: (0, 0, 255, 255),
                        1: (255, 255, 0, 255),
                        2: (0, 255, 0, 255),
                        3: (255, 0, 0, 255),
                    },
                )

    # Calculating the kelp pixels
    with Image.open(komp + ext1) as im:
        # If species differentiation is turned off
        if spec == False or spec == "0":
            for pixel in im.getdata():
                if pixel == 0:  # if your image is RGB (if RGBA, (0, 0, 0, 255) or so
                    no_kelp += 1
                elif pixel == 1:
                    kelp += 1
        # If species differentiation is turned on
        elif spec == True or spec == "1":
            for pixel in im.getdata():
                if pixel == 0:  # if your image is RGB (if RGBA, (0, 0, 0, 255) or so
                    no_kelp += 1
                elif pixel == 1:
                    kelp += 1
                elif pixel == 2:
                    giant += 1
                elif pixel == 3:
                    bull += 1

    # Calculating the area of the kelp in cm & acres
    kcm = kelp * (gsd * gsd)
    kacres = kcm * 0.000000024711

    bcm = bull * (gsd * gsd)
    bacres = bcm * 0.000000024711

    gcm = giant * (gsd * gsd)
    gacres = gcm * 0.000000024711

    # Printing the kelp surface area onto a .txt file
    with open(komp + ext2, "a") as f:
        # If species differentiation is turned off
        if spec == False or spec == "0":
            f.write("kelp area cm^2: " + str(kcm))
            # This should be .0001 because the conversion from cm^2 to m^2 is different than the conversion of cm to m!
            f.write("\nkelp area m^2: " + str(kcm * 0.0001))
            f.write("\nkelp area acres: " + str(kacres))
            f.write("\nno kelp pixels=" + str(no_kelp) + ", kelp pixels=" + str(kelp))
            print("kelp area (cm^2):" + str(kcm))
            print("kelp area (acres):" + str(kacres))
            print("no kelp pixels=" + str(no_kelp) + ", kelp pixels=" + str(kelp))

        # If species differentiation is turned off
        elif spec == True or spec == "1":
            f.write(
                "bull kelp area cm^2="
                + str(bcm)
                + ", bull kelp area acres="
                + str(bacres)
            )
            f.write(
                "\ngiant kelp area cm^2="
                + str(gcm)
                + ", giant kelp area acres="
                + str(gacres)
            )
            f.write(
                "\nbull kelp pixels=" + str(bull) + ", giant kelp pixels=" + str(giant)
            )
            print("bull kelp area (acres):" + str(bacres))
            print("giant kelp area (acres):" + str(gacres))
            print(
                "no kelp pixels="
                + str(no_kelp)
                + ", bull kelp pixels="
                + str(bull)
                + ", giant kelp pixels="
                + str(giant)
            )


""" --------------------- EXTRACT_ESSENTIALS FUNCTION ----------------------
This function takes a directory and grabs the ODM report and orthomosaic.
:param dir: The directory where the files are stored.
:param dest: The directory where the files are placed.
------------------------------------------------------------------------ """


def extract_essentials(dir: str, dest: str):
    shutil.copy(dir + "\\code\\odm_report\\report.pdf", dest)
    shutil.copy(dir + "\\code\\odm_orthophoto\\odm_orthophoto.tif", dest)


""" ------------------------- CALCULATE_GSD FUNCTION -----------------------
This function takes the pdf report from ODM and scrapes the GSD value from it.
This solution is very janky, but this was the only way I could do what I
wanted to do.
:param pdfdir: The directory where the pdf is stored.
------------------------------------------------------------------------ """


def calculate_gsd(pdfdir: str):
    pdfFileObj = open(pdfdir, "rb")
    # create a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    # creating a page object
    pageObj = pdfReader.pages[0]
    # extract text from page
    pdf = pageObj.extract_text()

    words = pdf.split(" ")
    # if "(GSD)" in words:
    #    pos = words.index("(GSD)")

    try:
        pos = words.index("(GSD)")
        res = words[pos + 1]

    except:
        print("Cannot find ground sampling distance.")

    # closing the pdf file object
    pdfFileObj.close()

    return res


""" ------------------------- COMPRESS_TIF FUNCTION -----------------------
This function takes a .tif file and compresses it, turning it into a viewable JPG file.
:param imgname: The path where the image is stored.
:param savename: The path where the new JPG is saved to.
------------------------------------------------------------------------ """


def compress_tif(imgname: str, savename: str):
    img = Image.open(imgname)
    rgb_im = img.convert("RGB")
    rgb_im.save(savename, optimize=True, quality=65)
