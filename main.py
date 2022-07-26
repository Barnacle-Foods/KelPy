# Barnacle imagery project main file
# File created: 6/28/2022
# Author: Chet Russell
# Last edited: 7/26/2022 - Chet Russell

from distutils.command.clean import clean
import os
import shutil
import PyPDF2
import hakai_segmentation
import rasterio
import zipfile
from PIL import Image
from glint_mask_tools import RGBThresholdMasker
from pyodm import Node, exceptions

""" ------------------------ MASKER FUNCTION ---------------------------
This function takes an image directory and a pixel buffer and runs the
glint-mask-tools python package.
:param imgdir: The directory where the images are stored.
:param pb: The value the glint-mask-tools package takes when calculating
           pixels affected.
------------------------------------------------------------------------ """


def masker(imgdir: str, pb: int):
    # This is the function that creates the image mask using glint-mask-tools.
    masker = RGBThresholdMasker(img_dir=imgdir, mask_dir=imgdir, pixel_buffer=pb)
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
------------------------------------------------------------------------ """


def orthorec(
    imgdir: str, dwndir: str, quality: str, crop: int, kmz: bool, ft: str, exif: bool
):
    imglist = []

    # Places each image filepath into the imglist list.
    for filenames in os.listdir(imgdir):
        tmp = imgdir + "/" + filenames
        imglist.append(tmp)

    n = Node("localhost", 3000)

    try:
        # Start a task
        print("Uploading images...")
        task = n.create_task(
            imglist,
            skip_post_processing=True,
            options={
                "orthophoto-cutline": False,
                "min-num-features": 20000,
                "pc-quality": quality,
                "texturing-data-term": "gmi",
                "verbose": True,
                "debug": True,
                "time": True,
                "crop": crop,
                "auto-boundary": False,
                "skip-3dmodel": True,
                "cog": False,
                "use-3dmesh": False,
                "pc-tile": True,
                "orthophoto-kmz": kmz,
                "use-exif": exif,
                "orthophoto-resolution": 1,
                "no-gpu": False,
                "ignore-gsd": False,
                "fast-orthophoto": True,
                "feature-type": ft,
            },
        )
        print(task.info())

        try:
            # This will block until the task is finished
            # or will raise an exception
            task.wait_for_completion()

            print("Task completed, downloading results...")

            # Retrieve results
            zipdir = task.download_zip(dwndir)
            with zipfile.ZipFile(zipdir, "r") as zip_ref:
                zip_ref.extractall(dwndir)

            # Removes mask files from the image folder.
            clean_masks(imgdir)

            extract_essentials(dwndir, True)

        except exceptions.TaskFailedError as e:
            print("\n".join(task.output()))
    except exceptions.NodeConnectionError as e:
        print("Cannot connect: %s" % e)
    except exceptions.NodeResponseError as e:
        print("Error: %s" % e)


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
NOT IMPLEMENTED:
:param spec: Wether kelpomatic should attempt to identify kelp species.
------------------------------------------------------------------------ """


def seg(ortho: str, komp: str, gsd: float, spec: bool):
    Image.MAX_IMAGE_PIXELS = 9999999999
    kelp = 0
    no_kelp = 0
    bull = 0
    giant = 0

    kom = komp + "/kelpomatic.tif"

    # Calling the kelpomatic tool
    hakai_segmentation.find_kelp(ortho, kom, species=spec, use_gpu=True)

    # Writing the colormap
    with rasterio.Env():

        with rasterio.open(kom) as src:
            shade = src.read(1)
            meta = src.meta

        with rasterio.open(komp + "/colormap.tif", "w", **meta) as dst:
            dst.write(shade, indexes=1)
            dst.write_colormap(
                1,
                {
                    0: (0, 0, 255, 255),
                    1: (255, 255, 0, 255),
                    # 2: (0, 255, 0, 255),
                    # 3: (255, 0 , 0, 255)
                },
            )
            cmap = dst.colormap(1)
            # True
            assert cmap[0] == (0, 0, 255, 255)
            # True
            assert cmap[1] == (255, 255, 0, 255)
            ## True
            # assert cmap[2] == (0, 255, 0, 255)
            ## True
            # assert cmap[3] == (255, 0 , 0, 255)

    # Calculating the kelp pixels
    with Image.open(komp + "/colormap.tif") as im:

        for pixel in im.getdata():
            if pixel == 0:  # if your image is RGB (if RGBA, (0, 0, 0, 255) or so
                no_kelp += 1
            elif pixel == 1:
                kelp += 1
            # elif pixel == 2:
            #    giant += 1
            # elif pixel == 3:
            #    bull += 1

    # Calculating the area of the kelp in cm & acres
    kcm = kelp * (gsd * gsd)
    kacres = kcm * 0.000000024711

    bcm = bull * (gsd * gsd)
    bacres = bcm * 0.000000024711

    gcm = giant * (gsd * gsd)
    gacres = gcm * 0.000000024711

    # Printing the kelp surface area onto a .txt file
    with open(komp + "/kelp_area.txt", "a") as f:
        f.write("kelp area cm^2: " + str(kcm))
        f.write("kelp area m^2: " + str(kcm * 0.01))
        f.write("\nkelp area acres: " + str(kacres))
        f.write("\nno kelp pixels=" + str(no_kelp) + ", kelp pixels=" + str(kelp))
        # f.write('\nbull kelp pixels=' + str(bull)+', giant kelp pixels='+str(giant))
        # f.write('\nbull kelp area acres=' + str(bacres)+', giant kelp acres='+str(gacres))

    extract_essentials(komp, False)

    print("no kelp pixels=" + str(no_kelp) + ", kelp pixels=" + str(kelp))
    print("kelp area (cm^2):" + str(kcm))
    print("kelp area (acres):" + str(kacres))

    return (
        "kelp area cm^2: "
        + str(kcm)
        + "\nkelp area m^2: "
        + str(kcm * 0.01)
        + "\nkelp area acres: "
        + str(kacres)
        + "\nno kelp pixels="
        + str(no_kelp)
        + ", kelp pixels="
        + str(kelp)
    )


""" ---------------------------- CLEAN_MASK FUNCTION -----------------------
This function takes an image directory and deletes all mask files located
within.
:param imgdir: The directory where the images are stored.
------------------------------------------------------------------------ """


def clean_masks(imgdir: str):
    for filename in os.listdir(imgdir):
        infilename = os.path.join(imgdir, filename)
        if not os.path.isfile(infilename):
            continue
        if infilename.endswith("_mask.JPG"):
            os.remove(infilename)


""" --------------------- EXTRACT_ESSENTIALS FUNCTION ----------------------
This function takes a directory and deletes all files except for the ODM
report, the orthomosaic, the kmz file, the colormap and the kelp area report.
:param imgdir: The directory where the files are stored.
:param ext: Boolean value to determine if the report and orthophoto should be
            grabbed.
------------------------------------------------------------------------ """


def extract_essentials(dir: str, ext: bool):
    if ext == True:
        os.replace(dir + "/odm_report/report.pdf", dir + "/report.pdf")
        os.replace(
            dir + "/odm_orthophoto/odm_orthophoto.tif", dir + "/odm_orthophoto.tif"
        )

    for filename in os.listdir(dir):
        infilename = os.path.join(dir, filename)
        if (
            infilename.endswith("report.pdf")
            or infilename.endswith("odm_orthophoto.tif")
            or infilename.endswith("colormap.tif")
            or infilename.endswith(".KML")
            or infilename.endswith("kelp_area.txt")
        ):
            continue
        elif infilename.endswith(".zip"):
            os.remove(infilename)
        elif infilename.endswith(".json"):
            os.remove(infilename)
        elif os.path.isdir(infilename):
            shutil.rmtree(infilename)
        else:
            os.remove(infilename)


""" ------------------------- CALCULATE_GSD FUNCTION -----------------------
This function takes the pdf report from ODM and scrapes the GSD value from it.
This solution is very janky, but this was the only way I could do what I
wanted to do.
:param pdfdir: The directory where the pdf is stored.
------------------------------------------------------------------------ """


def calculate_gsd(pdfdir: str):
    pdfFileObj = open(pdfdir, "rb")
    # create a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # creating a page object
    pageObj = pdfReader.getPage(0)
    # extract text from page
    pdf = pageObj.extractText()

    words = pdf.split(" ")
    if "(GSD)" in words:
        pos = words.index("(GSD)")

    tmp = words[pos + 1]
    # closing the pdf file object
    pdfFileObj.close()

    return tmp


""" ------------------------- RESIZE FUNCTION -----------------------
This function takes the pdf report from ODM and scrapes the GSD value from it.
:param imgpath: The directory where the image is stored.
------------------------------------------------------------------------ """

# def resize(imgpath: str):
